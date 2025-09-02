import React from 'react';

const Question = ({ question, currentAnswer, onAnswer }) => {
    const labels = {
        1: "Категорически не согласен",
        2: "Скорее не согласен",
        3: "Ни да ни нет",
        4: "Скорее согласен", 
        5: "Полностью согласен"
    };

    const handleAnswerChange = (value) => {
        onAnswer(question.id, value);
    };

    return (
        <div className="question-card">
            <h3 className="question-text">{question.text}</h3>
            
            <div className="likert-scale">
                {[1, 2, 3, 4, 5].map(value => (
                    <label key={value} className="likert-item">
                        <input
                            type="radio"
                            name={`question-${question.id}`}
                            value={value}
                            checked={currentAnswer === value}
                            onChange={() => handleAnswerChange(value)}
                            className="radio-input"
                        />
                        <span className="radio-custom"></span>
                        <span className="label-text">{labels[value]}</span>
                    </label>
                ))}
            </div>
        </div>
    );
};

export default Question;