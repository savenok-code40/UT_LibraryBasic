pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                echo 'Скачивание проекта из GitHub..'
            }
        }
        stage('Run CODESYS') {
            steps {
				echo 'Запуск CODESYS в фоновом режиме...'
				bat '"C:\\Program Files (x86)\\CODESYS 3.5.19.20\\CODESYS\\Common\\CODESYS.exe" --profile="CODESYS V3.5 SP19 Patch 2" --runscript="%WORKSPACE%\\run_tests.py" --noUI'
            
            }
        }
    }
}