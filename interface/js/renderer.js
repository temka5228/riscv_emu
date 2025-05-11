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
    const loadText = document.getElementById('load-text');
    const loadData = document.getElementById('load-data');

    const runBtn = document.getElementById('button-start');
    //const pauseBtn = document.getElementById('button-pause');
    const stopBtn = document.getElementById('button-stop');
    
    const textAddress = document.getElementById('text-address');
    const dataAddress = document.getElementById('data-address');
    const memorySize = document.getElementById('memory-size');
    const predictorSelector = document.getElementById('branch-predictor');
    const modelSelector = document.getElementById('model-selection');
    const usePredictor = document.getElementById('use-predictor');

    const fileName = document.getElementById('file-name');
    const terminal = document.getElementById('console');

    const status = document.getElementById('running');
    const predictorType = document.getElementById('predictor');
    const executionTime = document.getElementById('time');
    const Accuracy = document.getElementById('accuracy');
    const ROCAUC = document.getElementById('rocauc');
    const cyclesCount = document.getElementById('cycles');


    // Инициализация редактора кода
    codeEditor.innerHTML = '// Your code here';
    riscvAPI.selectPredictor(predictorSelector.value);
    riscvAPI.useBranch(usePredictor.checked)
    riscvAPI.setMemorySize(parseInt(memorySize.value))
    modelSelector.disabled = predictorSelector.value === 'mlpredictor' ? false:true;

    let base64String = '';


    // Обработчик загрузки файла
    uploader.addEventListener("change", async () => {
        var f = uploader.files[0];
        fname = uploader.value.split('\\').pop()
        const arrayBuffer = await f.arrayBuffer();
        base64String = btoa(String.fromCharCode(...new Uint8Array(arrayBuffer)));
    });

    uploadBtn.addEventListener('click', () => {
        uploader.click();
    });

    loadText.addEventListener('click', async () => {
        responseOk = await riscvAPI.loadFile(base64String, parseInt(textAddress.value));
        if (responseOk) {
            responseJson = await riscvAPI.decodeProgramm();
            updateTable();
            fileName.innerText = fname;
            codeEditor.innerHTML = responseJson['bytes'];
            outputConsole.innerHTML = responseJson['decoded'];
        }
    })

    loadData.addEventListener('click', async () => {
        await riscvAPI.loadFile(base64String, parseInt(dataAddress.value))
    })
    
    runBtn.addEventListener('click', async () => {
        status.innerHTML = 'running...';
        const responseRun = await riscvAPI.startEmulation(parseInt(textAddress.value));
        if (responseRun.ok) {
            updateTable();
            const runJson = responseRun.json
            status.innerText = 'completed'
            executionTime.innerText = runJson.time.toFixed(4)
            Accuracy.innerText = runJson.accuracy
            ROCAUC.innerText = runJson.rocauc
            cyclesCount.innerText = runJson.cycles
        }
        else {
            status.innerHTML = 'terminated'
            executionTime.innerHTML = '0.0000'
        }
    })

    stopBtn.addEventListener('click', () => {
        riscvAPI.stop();
    })


    predictorSelector.addEventListener('change', async () => {
        response = await riscvAPI.selectPredictor(predictorSelector.value)
        if (predictorSelector.value === 'mlpredictor') {
            modelSelector.disabled = false;
            if (response.ok) {
                riscvAPI.selectModel(modelSelector.value)
                predictorType.innerText = modelSelector.options[modelSelector.selectedIndex].text;  
            }
        }
        else {
            modelSelector.disabled = true;
            predictorType.innerText = predictorSelector.options[predictorSelector.selectedIndex].text;
        }
    })

    modelSelector.addEventListener('change', () => {
        riscvAPI.selectModel(modelSelector.value)
        predictorType.innerText = modelSelector.options[modelSelector.selectedIndex].text;
    })

    usePredictor.addEventListener('change', () => {
        riscvAPI.useBranch(usePredictor.checked)
        predictorType.innerText = usePredictor.checked ? 
            modelSelector.disabled ? 
            predictorSelector.options[predictorSelector.selectedIndex].text:
            modelSelector.options[modelSelector.selectedIndex].text: 
            'None'
    })

    memorySize.addEventListener('change', () => {
        textAddress.max = memorySize.value;
        riscvAPI.setMemorySize(parseInt(memorySize.value))
    })

    textAddress.addEventListener('change', () => {
        riscvAPI.setStartAddress(parseInt(textAddress.value))
    })

    riscvAPI.onConsoleOutput((data) => {
        terminal.innerText += data;
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