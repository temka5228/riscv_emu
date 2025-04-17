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
    async function readFile() {
        var f = uploader.files[0];
        const arrayBuffer = await f.arrayBuffer();
        const  base64String = btoa(String.fromCharCode(...new Uint8Array(arrayBuffer)));
        responseOk = await riscvAPI.loadFile(base64String, 4)
        if (responseOk) {
            responseText = await riscvAPI.decodeProgramm()
            console.log(arrayBuffer)
            outputConsole.innerHTML = responseText
        }
    }

    uploader.addEventListener("change", readFile);

    uploadBtn.addEventListener('click', () => {
        uploader.click();
    });
    
    runBtn.addEventListener('click', async () => {
        riscvAPI.startEmulation()
    })

    pauseBtn.addEventListener('click', () => {
    })

    // Обработчик для переключения между таблицей памяти и таблицей регистров
    memoryBtn.addEventListener('click', async () => {
        responseMemory = await riscvAPI.getMemory();
        registerBtn.classList.remove('active');
        memoryBtn.classList.add('active');
        tableContainer.innerHTML = jsonToTable(responseMemory)
    });

    registerBtn.addEventListener('click', async () => {
        responseRegisters = await riscvAPI.getRegisters();
        memoryBtn.classList.remove('active');
        registerBtn.classList.add('active');
        tableContainer.innerHTML = jsonToTable(responseRegisters)
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

    function jsonToTable(jsonData) {
        let table = ''
        for (const [key, value] of Object.entries(jsonData)) {
            table += '<tr>';
            table += `<td>${key}</td><td>${value}</td>`;
            table += '</tr>';
        }
        return table;
    }

    side_buttons[0].click();
    registerBtn.click();
});