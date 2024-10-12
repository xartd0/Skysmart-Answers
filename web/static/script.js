async function getAnswers() {
    const roomName = document.getElementById('roomName').value;
    if (roomName) {

        document.getElementById('loading').classList.remove('hidden');

        try {
            const response = await fetch('https://skysmart-answers.vercel.app/get_answers/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: "include",  
                body: JSON.stringify({ roomName })
            });
            const data = await response.json(); // Получаем данные от API
            const answers = data[0]; // Ответы находятся в первом объекте
            const testInfo = data["1"];

            displayTestInfo(testInfo);

            // Отображение ответов
            const answersDiv = document.getElementById('answers');
            answersDiv.innerHTML = ''; // Очистка предыдущих ответов
            answers.forEach((answer, index) => {
                const formattedAnswer = formatAndCheckLatex(answer.answers);
                const answerHtml = `
                    <div class="bg-white p-4 rounded shadow-md mb-4 opacity-0 transition-opacity duration-500" style="animation-delay: ${index * 100}ms">
                        <p class="text-gray-800">Задание #${answer.task_number} - ${answer.question}</p>
                        <p class="text-indigo-600">Ответ: ${formattedAnswer}</p>
                    </div>
                `;
                answersDiv.innerHTML += answerHtml;
            });

            // Скрываем индикатор загрузки
            document.getElementById('loading').classList.add('hidden');

            // Анимация появления каждого блока
            document.querySelectorAll('#answers > div').forEach(div => {
                div.classList.add('animate-fadeIn');
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

function displayTestInfo(info) {
    // Извлекаем необходимую информацию
    const title = info.title;
    const moduleTitle = info.meta.path.module.title;
    const subjectTitle = info.meta.subject.title;
    const teacherName = `${info.meta.teacher.name} ${info.meta.teacher.surname}`;
    const workbookTitle = info.meta.workbook.workbook.title;
    const lessonTitle = info.meta.path.module.lesson.title;
    const createdAt = new Date(info.createdAt); // Преобразуем строку времени в объект Date

    // Формируем строку с датой и временем в удобочитаемом формате
    const dateTimeStr = createdAt.toLocaleString('ru-RU', { dateStyle: 'long', timeStyle: 'short' });

    // Формируем HTML для информации о тесте
    const testInfoHtml = `
        <h2 class="text-lg font-bold">${title}</h2>
        <p><strong>Модуль:</strong> ${moduleTitle}</p>
        <p><strong>Урок:</strong> ${lessonTitle}</p>
        <p><strong>Предмет:</strong> ${subjectTitle}</p>
        <p><strong>Преподаватель:</strong> ${teacherName}</p>
        <p><strong>Рабочая тетрадь:</strong> ${workbookTitle}</p>
        <p><strong>Время создания:</strong> ${dateTimeStr}</p>
    `;

    // Добавляем информацию в DOM и показываем блок
    const testInfoDiv = document.getElementById('testInfo');
    testInfoDiv.innerHTML = testInfoHtml;
    testInfoDiv.classList.remove('hidden');
}