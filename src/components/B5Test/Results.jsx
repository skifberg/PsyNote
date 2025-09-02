import React from 'react';

const Results = ({ data, onRestart }) => {
    const { scores, interpretation } = data;
    
    const factorNames = {
        E: { name: 'Экстраверсия', color: '#4CAF50' },
        A: { name: 'Доброжелательность', color: '#2196F3' },
        C: { name: 'Добросовестность', color: '#FF9800' },
        N: { name: 'Нейротизм', color: '#F44336' },
        O: { name: 'Открытость опыту', color: '#9C27B0' }
    };

    const getLevelLabel = (level) => {
        switch (level) {
            case 'high': return 'Высокий';
            case 'medium': return 'Средний';
            case 'low': return 'Низкий';
            default: return level;
        }
    };

    return (
        <div className="results-container">
            <div className="results-header">
                <h2>Ваши результаты теста Big Five</h2>
                <p>Вот ваш личностный профиль по пяти основным факторам:</p>
            </div>
            
            <div className="results-grid">
                {Object.entries(interpretation).map(([factor, data]) => (
                    <div key={factor} className="factor-card">
                        <div className="factor-header">
                            <h3 style={{ color: factorNames[factor].color }}>
                                {factorNames[factor].name}
                            </h3>
                            <span className={`level-badge level-${data.level}`}>
                                {getLevelLabel(data.level)}
                            </span>
                        </div>
                        
                        <div className="score-display">
                            <div className="score-value">
                                {data.score} / {data.max_score}
                            </div>
                            <div className="score-bar">
                                <div 
                                    className="score-fill"
                                    style={{ 
                                        width: `${(data.score / data.max_score) * 100}%`,
                                        backgroundColor: factorNames[factor].color
                                    }}
                                ></div>
                            </div>
                        </div>

                        <div className="interpretation">
                            <p>{data.interpretation}</p>
                        </div>
                    </div>
                ))}
            </div>

            <div className="results-summary">
                <h3>Ваш личностный профиль</h3>
                <p>
                    {interpretation.E.level === 'high' ? 'Общительный' : 'Сдержанный'}, 
                    {interpretation.A.level === 'high' ? ' доброжелательный' : ' прямолинейный'}, 
                    {interpretation.C.level === 'high' ? ' организованный' : ' спонтанный'}, 
                    {interpretation.N.level === 'high' ? ' чувствительный' : ' устойчивый'}, 
                    {interpretation.O.level === 'high' ? ' открытый новому' : ' практичный'}
                </p>
            </div>

            <div className="results-actions">
                <button onClick={onRestart} className="restart-button">
                    Пройти тест снова
                </button>
                <button onClick={() => window.print()} className="print-button">
                    Распечатать результаты
                </button>
            </div>
        </div>
    );
};

export default Results;