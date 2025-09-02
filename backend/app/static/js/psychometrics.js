class PsychometricsApp {
    constructor() {
        this.currentTest = null;
        console.log("PsychometricsApp инициализирован");
        this.init();
    }

    async init() {
        console.log("Загрузка тестов...");
        await this.loadTests();
        this.setupEventListeners();
    }

    async loadTests() {
        try {
            console.log("Запрос к API...");
            const response = await fetch('/api/psychometrics/tests');
            console.log("Ответ получен, статус:", response.status);
            
            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }
            
            const tests = await response.json();
            console.log("Тесты загружены:", tests);
            this.renderTests(tests);
        } catch (error) {
            console.error('Ошибка загрузки тестов:', error);
            this.showError('Не удалось загрузить тесты: ' + error.message);
        }
    }

    renderTests(tests) {
        const container = document.getElementById('tests-container');
        
        if (!tests || tests.length === 0) {
            container.innerHTML = `
                <div class="error">
                    <p>Тесты не найдены</p>
                    <button onclick="app.loadTests()">Попробовать снова</button>
                </div>
            `;
            return;
        }

        container.innerHTML = '';
        tests.forEach(test => {
            const card = document.createElement('div');
            card.className = 'test-card';
            card.innerHTML = `
                <h3>${test.name}</h3>
                <p>${test.description}</p>
                <div class="test-meta">
                    <span class="question-count">📝 ${test.question_count} вопросов</span>
                </div>
                <button class="test-button" onclick="app.startTest('${test.id}')">
                    🚀 Начать тест
                </button>
            `;
            container.appendChild(card);
        });
    }

    async startTest(testId) {
        try {
            console.log("Загрузка теста:", testId);
            const response = await fetch(`/api/psychometrics/tests/${testId}`);
            console.log("Ответ теста, статус:", response.status);
            
            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }
            
            this.currentTest = await response.json();
            console.log("Тест загружен:", this.currentTest);
            this.showTest();
        } catch (error) {
            console.error('Ошибка загрузки теста:', error);
            this.showError('Не удалось загрузить тест: ' + error.message);
        }
    }

    showTest() {
        this.hideAllSections();
        document.getElementById('test-section').classList.remove('hidden');
        
        document.getElementById('test-title').textContent = this.currentTest.name;
        document.getElementById('test-description').textContent = this.currentTest.description;
        
        const questionsContainer = document.getElementById('questions-container');
        questionsContainer.innerHTML = '';
        
        // Добавляем блок с инструкциями
        if (this.currentTest.instructions) {
            const instructionsDiv = document.createElement('div');
            instructionsDiv.className = 'instruction-box';
            instructionsDiv.innerHTML = `
                <h4>📋 Инструкция к тесту:</h4>
                <p>${this.currentTest.instructions}</p>
                <div class="instruction-note">
                    <strong>💡 Важно:</strong> Отвечайте честно, выбирая вариант, который наиболее точно 
                    описывает ваше состояние за последние 2 недели.
                </div>
            `;
            questionsContainer.appendChild(instructionsDiv);
        }
        
        // Добавляем вопросы
        this.currentTest.questions.forEach(question => {
            const questionDiv = document.createElement('div');
            questionDiv.className = 'question';
            questionDiv.innerHTML = `
                <h4>${question.id}. ${question.text}</h4>
                <div class="options">
                    ${question.options.map(option => `
                        <label class="option-label">
                            <input type="radio" name="question_${question.id}" value="${option.value}" required>
                            ${option.text}
                        </label>
                    `).join('')}
                </div>
            `;
            questionsContainer.appendChild(questionDiv);
        });
    }

    async submitTest(event) {
        event.preventDefault();
        
        const answers = [];
        this.currentTest.questions.forEach(question => {
            const selected = document.querySelector(`input[name="question_${question.id}"]:checked`);
            if (selected) {
                answers.push({
                    question_id: question.id,
                    value: parseInt(selected.value)
                });
            }
        });
        
        if (answers.length !== this.currentTest.questions.length) {
            alert('Пожалуйста, ответьте на все вопросы');
            return;
        }
        
        try {
            const response = await fetch(`/api/psychometrics/tests/${this.currentTest.id}/submit`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    test_id: this.currentTest.id,
                    answers: answers
                })
            });
            
            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }
            
            const results = await response.json();
            console.log("Результаты:", results);
            this.showResults(results);
        } catch (error) {
            console.error('Ошибка отправки теста:', error);
            alert('Ошибка отправки теста: ' + error.message);
        }
    }

    showResults(results) {
        document.getElementById('test-container').style.display = 'none';
        document.getElementById('results-container').style.display = 'block';
        
        const resultsContent = document.getElementById('results-content');
        resultsContent.innerHTML = `
            <div class="result-card">
                <h3>${results.test_name}</h3>
                <p class="score">Баллы: ${results.score} из ${results.max_score}</p>
                
                <div class="interpretation">
                    <h4>${results.interpretation.result}</h4>
                    <p>${results.interpretation.description}</p>
                </div>
                
                ${results.interpretation.recommendations && results.interpretation.recommendations.length ? `
                    <div class="recommendations">
                        <h5>💡 Рекомендации:</h5>
                        <ul>
                            ${results.interpretation.recommendations.map(rec => 
                                `<li>${rec}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
                
                <div class="disclaimer">
                    <h5>⚠️ Важная информация:</h5>
                    <p>Этот тест является скрининговым инструментом и не заменяет профессиональную диагностику. 
                    Если ваши результаты вызывают беспокойство, рекомендуется обратиться к психологу или психотерапевту 
                    для получения квалифицированной помощи.</p>
                    <p class="disclaimer-note">
                        <strong>Помните:</strong> Депрессия - это treatable состояние, и профессиональная помощь 
                        может значительно улучшить качество жизни.
                    </p>
                </div>
                
                <div class="resources">
                    <h5>📞 Полезные ресурсы:</h5>
                    <ul>
                        <li>Телефон доверия: 8-800-2000-122 (круглосуточно, бесплатно)</li>
                        <li>Экстренная психологическая помощь: 112</li>
                        <li>Обратитесь к своему терапевту для направления к специалисту</li>
                    </ul>
                </div>
            </div>
        `;
    }

    showError(message) {
        const container = document.getElementById('tests-container');
        container.innerHTML = `
            <div class="error">
                <p>${message}</p>
                <button onclick="location.reload()">Перезагрузить страницу</button>
            </div>
        `;
    }

    hideAllSections() {
        document.getElementById('tests-section').classList.add('hidden');
        document.getElementById('test-section').classList.add('hidden');
        document.getElementById('results-section').classList.add('hidden');
    }

    setupEventListeners() {
        const form = document.getElementById('test-form');
        if (form) {
            form.addEventListener('submit', (e) => this.submitTest(e));
        }
    }
}

// Инициализация приложения
document.addEventListener('DOMContentLoaded', function() {
    window.app = new PsychometricsApp();
});