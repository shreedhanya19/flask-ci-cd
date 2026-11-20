
pipeline {
    agent any

    environment {
        APP_PORT = '5001'
    }

    stages {

        // STAGE 1: BUILD
        stage('Build') {
            steps {
                echo 'Building Flask environment'

                sh '''
                    set -eu

                    python3 --version

                    python3 -m venv .venv

                    . .venv/bin/activate

                    python -m pip install -r requirements.txt
                '''
            }
        }

        // STAGE 2: TEST
        stage('Test') {
            steps {
                echo 'Running unit tests'

                sh '''
                    set -eu

                    . .venv/bin/activate

                    python -m unittest discover -s tests -v
                '''
            }
        }

        // STAGE 3: DEPLOY
        stage('Deploy') {
            steps {
                echo 'Deploying application copy'

                sh '''
                    set -eu

                    DEPLOY_DIR="$WORKSPACE/deployment"

                    # Stop previous application if running
                    if [ -f "$DEPLOY_DIR/app.pid" ]; then
                        OLD_PID=$(cat "$DEPLOY_DIR/app.pid")

                        if kill -0 "$OLD_PID" 2>/dev/null; then
                            kill "$OLD_PID" || true
                            sleep 2
                        fi
                    fi

                    # Create a fresh deployment directory
                    rm -rf "$DEPLOY_DIR"
                    mkdir -p "$DEPLOY_DIR"

                    # Copy application files
                    cp app.py requirements.txt "$DEPLOY_DIR/"

                    # Record deployment build number
                    echo "$BUILD_NUMBER" > "$DEPLOY_DIR/deployed-build.txt"

                    echo "Application copied successfully"
                '''
            }
        }

        // STAGE 4: RUN APPLICATION
        stage('Run Application') {
            steps {
                echo 'Starting deployed Flask application'

                sh '''
                    set -eu

                    DEPLOY_DIR="$WORKSPACE/deployment"

                    cd "$DEPLOY_DIR"

                    # Keep the background process alive after the build
                    export JENKINS_NODE_COOKIE=dontKillMe

                    # Start Flask in the background
                    nohup env PORT="$APP_PORT" \
                    "$WORKSPACE/.venv/bin/python" app.py \
                    > app.log 2>&1 &

                    echo $! > app.pid

                    echo "Flask application started"
                '''
            }
        }

        // STAGE 5: TEST APPLICATION
        stage('Test Application') {
            steps {
                echo 'Verifying deployed application'

                sh '''
                    set -eu

                    DEPLOY_DIR="$WORKSPACE/deployment"
                    URL="http://127.0.0.1:${APP_PORT}/"

                    # Wait for application startup
                    READY=0

                    for i in $(seq 1 20); do
                        if curl -sS "$URL" -o /dev/null; then
                            READY=1
                            break
                        fi

                        sleep 1
                    done

                    if [ "$READY" -ne 1 ]; then
                        echo "Application failed to start"
                        cat "$DEPLOY_DIR/app.log"
                        exit 1
                    fi

                    # Get HTTP status and response body
                    HTTP_CODE=$(curl -sS \
                    -o "$DEPLOY_DIR/response.txt" \
                    -w "%{http_code}" "$URL")

                    BODY=$(cat "$DEPLOY_DIR/response.txt")

                    echo "HTTP Status: $HTTP_CODE"
                    echo "Response Body: $BODY"

                    # Verify status code
                    test "$HTTP_CODE" = "200"

                    # Verify response body
                    echo "$BODY" | grep -Fq \
                    "Hello from Flask CI/CD pipeline!"

                    echo "Application verification successful"
                '''
            }
        }
    }

    // POST BUILD ACTIONS
    post {

        success {
            echo 'SUCCESS: CI/CD Pipeline completed successfully!'
        }

        failure {
            echo 'FAILURE: CI/CD Pipeline failed. Check console logs!'
        }

        always {
            echo 'Pipeline execution finished.'
        }
    }
}
