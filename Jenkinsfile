pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                echo 'Скачиваем код из GitHub...'
            }
        }
        stage('Build & Test') {
            steps {
                echo 'Запускаем тесты 1С...'
                // Сюда мы позже впишем команду запуска твоих тестов
                sh 'java -version' 
            }
        }
    }
}