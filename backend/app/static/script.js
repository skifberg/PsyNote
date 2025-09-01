function selectChoice(choice) {
    console.log('Выбран вариант:', choice);
    
    if (choice === 'iching') {
        // Переход к Книге Перемен
        window.location.href = '/api/iching/';
    } else {
        // Временная заглушка для других вариантов
        alert('Этот модуль в разработке. Вы выбрали: ' + choice);
        
        // Здесь потом будет переход к другим модулям
        // if (choice === 'self-analysis') {
        //     window.location.href = '/self-analysis/';
        // } else if (choice === 'testing') {
        //     window.location.href = '/testing/';
        // }
    }
}