async function getHexagram() {
    try {
        const response = await fetch('/api/iching/random-hexagram');
        const data = await response.json();
        
        document.getElementById('hexagramSymbol').textContent = data.data.symbol || '⚪';
        document.getElementById('hexagramName').textContent = 
            `${data.data.number}. ${data.data.name}`;
        document.getElementById('adviceText').textContent = 
            `${data.data.meaning}\n\nСовет: ${data.data.advice}`;
            
    } catch (error) {
        console.error('Error:', error);
    }
}

async function castCoins() {
    try {
        const response = await fetch('/api/iching/cast-hexagram');
        const data = await response.json();
        
        const coins = data.coins_result.map(coin => coin === 2 ? '⚪' : '⚫').join(' ');
        
        document.getElementById('hexagramSymbol').textContent = data.hexagram.symbol;
        document.getElementById('hexagramName').textContent = 
            `${data.hexagram.number}. ${data.hexagram.name}`;
        document.getElementById('adviceText').innerHTML = 
            `Монеты: <span class="coins-result">${coins}</span><br>
             Тип линии: ${data.line_type}<br><br>
             ${data.hexagram.meaning}`;
            
    } catch (error) {
        console.error('Error:', error);
    }
}

async function getAdvice() {
    try {
        const response = await fetch('/api/iching/random-advice');
        const data = await response.json();
        
        document.getElementById('hexagramSymbol').textContent = '💫';
        document.getElementById('hexagramName').textContent = 'Совет судьбы';
        document.getElementById('adviceText').textContent = data.data;
            
    } catch (error) {
        console.error('Error:', error);
    }
}