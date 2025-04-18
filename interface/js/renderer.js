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
    const memoryAddress = document.getElementById('memory-address');
    const memorySize = document.getElementById('memory-size');
    const fileName = document.getElementById('file-name');
    const terminal = document.getElementById('console');

    // Инициализация редактора кода
    codeEditor.innerHTML = '// Your code here';

    // Обработчик загрузки файла
    async function readFile() {
        var f = uploader.files[0];
        fname = uploader.value.split('\\').pop()
        const arrayBuffer = await f.arrayBuffer();
        const  base64String = btoa(String.fromCharCode(...new Uint8Array(arrayBuffer)));
        responseOk = await riscvAPI.loadFile(base64String);
        if (responseOk) {
            responseJson = await riscvAPI.decodeProgramm();
            updateTable();
            fileName.innerText = fname;
            codeEditor.innerHTML = responseJson['bytes'];
            outputConsole.innerHTML = responseJson['decoded'];
        }
    }

    uploader.addEventListener("change", readFile);

    uploadBtn.addEventListener('click', () => {
        uploader.click();
    });
    
    runBtn.addEventListener('click', async () => {
        await riscvAPI.startEmulation();
        updateTable();
    })

    pauseBtn.addEventListener('click', () => {
    })

    memorySize.addEventListener('change', () => {
        memoryAddress.max = memorySize.value;

    })

    riscvAPI.onConsoleOutput((data) => {
        console.log(data);
        terminal.innerHTML += `${data}<br/>`;
        terminal.scroll({
            top: terminal.scrollHeight,
            behavior:'smooth'
        });
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

    async function updateTable() {
        if (registerBtn.classList.contains('active')) {
            responseRegisters = await riscvAPI.getRegisters();
            tableContainer.innerHTML = jsonToTable(responseRegisters)
        }
        else {
            responseMemory = await riscvAPI.getMemory();
            tableContainer.innerHTML = jsonToTable(responseMemory);
        }
    }
    side_buttons[0].click();
    registerBtn.click();
});