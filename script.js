async function getAnswers() {
    const roomName = document.getElementById('roomName').value;
    if (roomName) {
        try {
            const response = await fetch('http://localhost:8000/get_answers/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ roomName })
            });
            const answers = await response.json();

            // Отображение ответов
            const answersDiv = document.getElementById('answers');
            answersDiv.innerHTML = ''; // Очистка предыдущих ответов
            answers.forEach(answer => {
                // Форматирование и проверка на LaTeX
                const formattedAnswer = formatAndCheckLatex(answer.answer);
                answersDiv.innerHTML += `<p>Задание #${answer.task_number} - ${answer.question}<br>Ответ: ${formattedAnswer}</p>`;
            });

            // Обновление MathJax
            MathJax.typesetPromise().then(() => {
                console.log('MathJax обработал новый контент');
            }).catch(err => console.error('Ошибка MathJax: ', err));

        } catch (error) {
            console.error('Ошибка при получении ответов:', error);
        }
    } else {
        alert('Пожалуйста, введите название комнаты.');
    }
}

// Функция для форматирования ответа и обертывания LaTeX в разделители MathJax, если необходимо
function formatAndCheckLatex(text) {
    // Паттерн для поиска LaTeX в тексте
    const latexPattern = /\\[a-zA-Z]+|_{1,2}\{|\^/; // Добавьте другие паттерны по необходимости
    if (latexPattern.test(text)) {
        // Если текст содержит LaTeX, оборачиваем его в разделители MathJax
        return `\\(${text}\\)`;
    } else {
        // Если нет, возвращаем текст как есть
        return text;
    }
}
