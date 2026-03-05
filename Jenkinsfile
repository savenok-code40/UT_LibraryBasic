pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                echo 'Код скачан!'
            }
        }
        stage('Build & Test') {
            steps {
                // Сюда мы позже впишем команду запуска твоих тестов
                bat 'java -version' 
            }
        }
    }
}