document.addEventListener('DOMContentLoaded', () => {
    const codeEditor = document.getElementById('code-editor');
    const outputConsole = document.getElementById('output-console');
    const memoryBtn = document.getElementById('memory-btn');
    const registerBtn = document.getElementById('register-btn');
    const tableContainer = document.getElementById('table');

    // Инициализация редактора кода
    codeEditor.innerHTML = '// Your code here';

    // Обработчик для отправки запросов
 

    // Обработчик для переключения между таблицей памяти и таблицей регистров
    memoryBtn.addEventListener('click', () => {
        displayTable(memoryData);
    });

    registerBtn.addEventListener('click', () => {
        displayTable(registerData);
    });

    // Пример данных для таблицы памяти (замените на реальные данные из эмулятора)
    const memoryData = generateTableData(62, 2, 'Memory Address');
    const registerData = generateTableData(62, 2, 'Register');

    // Функция для генерации таблицы данных
    function generateTableData(rows, cols, header) {
        let tableHtml = ''//`<h3><td>${header}</td><td>Value</td></h3><table>`;
        for (let i = 0; i < rows; i++) {
            tableHtml += '<tr>';
            tableHtml += `<td>${header[0] + i}</td><td>${0}</td>`
            /*
            for (let j = 0; j < cols; j++) {
                tableHtml += `<td>X ${i * cols + j}</td>`;
            }
            */
            tableHtml += '</tr>';
        }
        tableHtml += '</table>';
        return tableHtml;
    }

    // Функция для отображения таблицы
    function displayTable(data) {
        tableContainer.innerHTML = data;
    }

    // Инициализация отображения по умолчанию (например, таблица памяти)
    displayTable(memoryData);
});