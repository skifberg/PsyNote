import React, { useState, useEffect } from 'react';
import Question from './Question';
import Results from './Results';
import './B5Test.css';

// Базовый URL для API
const API_BASE_URL = 'http://localhost:8000';

const B5Test = () => {
    const [questions, setQuestions] = useState([]);
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [answers, setAnswers] = useState({});
    const [isLoading, setIsLoading] = useState(true);
    const [showResults, setShowResults] = useState(false);
    const [results, setResults] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchQuestions();
    }, []);

    const fetchQuestions = async () => {
        try {
            setIsLoading(true);
            const response = await fetch(`${API_BASE_URL}/api/b5-test/questions`);
            const data = await response.json();
            
            if (data.success) {
                setQuestions(data.questions);
                setError(null);
            } else {
                setError(data.message || 'Ошибка загрузки вопросов');
            }
        } catch (error) {
            setError('Ошибка соединения с сервером');
            console.error('Error fetching questions:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleAnswer = (questionId, answerValue) => {
        setAnswers(prev => ({
            ...prev,
            [questionId]: answerValue
        }));
    };

    const handleNext = () => {
        if (currentQuestionIndex < questions.length - 1) {
            setCurrentQuestionIndex(prev => prev + 1);
        }
    };

    const handlePrevious = () => {
        if (currentQuestionIndex > 0) {
            setCurrentQuestionIndex(prev => prev - 1);
        }
    };

    const handleSubmit = async () => {
        try {
            setIsLoading(true);
            
            const answerArray = Object.entries(answers).map(([questionId, answerValue]) => ({
                questionId: parseInt(questionId),
                answerValue: answerValue
            }));

            const response = await fetch(`${API_BASE_URL}/api/b5-test/submit`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    answers: answerArray
                })
            });

            const data = await response.json();
            
            if (data.success) {
                setResults(data);
                setShowResults(true);
                setError(null);
            } else {
                setError(data.message || 'Ошибка обработки результатов');
            }
        } catch (error) {
            setError('Ошибка отправки ответов');
            console.error('Error submitting answers:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const restartTest = () => {
        setCurrentQuestionIndex(0);
        setAnswers({});
        setShowResults(false);
        setResults(null);
        setError(null);
    };

    if (isLoading && questions.length === 0) {
        return (
            <div className="loading-container">
                <div className="loading-spinner"></div>
                <p>Загрузка вопросов...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="error-container">
                <h3>Произошла ошибка</h3>
                <p>{error}</p>
                <button onClick={fetchQuestions} className="retry-button">
                    Попробовать снова
                </button>
            </div>
        );
    }

    if (showResults && results) {
        return <Results data={results} onRestart={restartTest} />;
    }

    const currentQuestion = questions[currentQuestionIndex];
    const progress = ((currentQuestionIndex + 1) / questions.length) * 100;

    return (
        <div className="b5-test-container">
            <div className="test-header">
                <h2>Тест личности Big Five</h2>
                <div className="progress-info">
                    Вопрос {currentQuestionIndex + 1} из {questions.length}
                </div>
            </div>

            <div className="progress-bar">
                <div 
                    className="progress-fill"
                    style={{ width: `${progress}%` }}
                ></div>
            </div>

            {currentQuestion && (
                <Question
                    question={currentQuestion}
                    currentAnswer={answers[currentQuestion.id] || null}
                    onAnswer={handleAnswer}
                />
            )}

            <div className="navigation-buttons">
                <button 
                    onClick={handlePrevious}
                    disabled={currentQuestionIndex === 0}
                    className="nav-button prev-button"
                >
                    ← Назад
                </button>
                
                {currentQuestionIndex === questions.length - 1 ? (
                    <button 
                        onClick={handleSubmit}
                        disabled={Object.keys(answers).length !== questions.length}
                        className="nav-button submit-button"
                    >
                        {isLoading ? 'Обработка...' : 'Завершить тест'}
                    </button>
                ) : (
                    <button 
                        onClick={handleNext}
                        disabled={!answers[currentQuestion?.id]}
                        className="nav-button next-button"
                    >
                        Далее →
                    </button>
                )}
            </div>

            <div className="answers-progress">
                Отвечено: {Object.keys(answers).length} / {questions.length}
            </div>
        </div>
    );
};

export default B5Test;