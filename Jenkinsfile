pipeline {
    agent any

    environment {
        imagename = "joon09/fastapi-torch"
        registryCredential = 'joon09'
        version = '1.1'
        dockerImage = ''
    }

    stages {

        // docker build
        stage('Bulid Docker') {
          agent any
          steps {
            echo 'Bulid Docker'
            script {
                dockerImage = docker.build imagename
            }
          }
          post {
            failure {
              error 'This pipeline stops here...'
            }
          }
        }

        // docker push
        stage('Push Docker') {
          agent any
          steps {
            echo 'Push Docker'
            script {
                docker.withRegistry( '', registryCredential) {
                    dockerImage.push(version)  // ex) "1.0"
                }
            }
          }
          post {
            failure {
              error 'This pipeline stops here...'
            }
          }
        }

        // docker Deploy
        stage('Deploy Docker') {
          agent any
          steps {
            echo 'Deploy Docker'
            sh 'docker-compose -f ./docker/docker-compose.yml up -d'
          }
          post {
            failure {
              error 'This pipeline stops here...'
            }
          }
        }

    }
}