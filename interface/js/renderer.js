document.addEventListener('DOMContentLoaded', () => {
    const codeEditor = document.getElementById('code-editor');
    const outputConsole = document.getElementById('output-console');
    const memoryBtn = document.getElementById('memory-btn');
    const registerBtn = document.getElementById('register-btn');
    const tableContainer = document.getElementById('table');
    const side_buttons = document.querySelectorAll('.sidebar button');
    const tabs = document.querySelectorAll('.tab-content');
    const tableBtns = document.querySelectorAll('.table-btn');
    const uploadBtn = document.getElementById('button-upload');
    const uploader = document.getElementById('uploadFile');
    const runBtn = document.getElementById('button-start');
    const pauseBtn = document.getElementById('button-pause');
    

    // Инициализация редактора кода
    codeEditor.innerHTML = '// Your code here';

    // Обработчик загрузки файла
    function readFile(file) {
        var f = uploader.files[0];
        var reader = new FileReader();
        var fileByteArray = [];
        reader.onloadend = (evt) => {
            var binaryString = evt.target.result;
            console.log('try to start emulator')
            window.riscvAPI.startEmulation(binaryString, 4)
        };
        reader.readAsBinaryString(f);

        //const reader = new FileReader();
        //reader.readAsArrayBuffer(f);
    }

    uploader.addEventListener("change", readFile);
    uploadBtn.addEventListener('click', () => {
        uploader.click();
    });
    // Обработчик для отправки запросов
    
    runBtn.addEventListener('click', () => {
        window.riscvAPI.startEmulation()
    })

    pauseBtn.addEventListener('click', () => {
        window.riscvAPI.getState()
    })

    // Обработчик для переключения между таблицей памяти и таблицей регистров
    memoryBtn.addEventListener('click', () => {
        displayTable(memoryData);
    });

    registerBtn.addEventListener('click', () => {
        displayTable(registerData);
    });


    side_buttons.forEach(button => {
        button.addEventListener('click', function(){
            const tabId = this.getAttribute('data-tab');
            side_buttons.forEach(btn => btn.classList.remove('active'));
            tabs.forEach(tab => tab.classList.remove('active'));
            this.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });

    tableBtns.forEach(btn => {
        btn.addEventListener('click', function(){
            tableBtns.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            const tableId = this.getAttribute('data-table');
            getTableById(tableId);
        });
    })

    
    // Пример данных для таблицы памяти (замените на реальные данные из эмулятора)
    function getTableById(tableId){
        console.log(tableId);
        switch (tableId){
            case "memory":
                return memoryData;
            case "register":
                return registerData;
        }
    }
    const memoryData = generateTableData(62, 2, 'Memory Address');
    const registerData = generateTableData(62, 2, 'Register');

    // Функция для генерации таблицы данных
    function generateTableData(rows, cols, header) {
        let tableHtml = ''//`<h3><td>${header}</td><td>Value</td></h3><table>`;
        for (let i = 0; i < rows; i++) {
            tableHtml += '<tr>';
            tableHtml += `<td>${header[0] + i}</td><td>${0}</td>`
            tableHtml += '</tr>';
        }
        tableHtml += '</table>';
        return tableHtml;
    }

    // Функция для отображения таблицы
    function displayTable(data) {
        tableContainer.innerHTML = data;
    }

    function openTab(tabID){
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        })
        document.getElementById(tabID).classList.add('active');
    }


    side_buttons[0].click();
    //initTitleBar()

    // Инициализация отображения по умолчанию (например, таблица памяти)
    displayTable(memoryData);
});