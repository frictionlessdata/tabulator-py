# Node
nvm install 4
nvm use 4
npm install

# Python
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements.dev.txt

# Git commit hook
if [ ! -f .git/hooks/pre-commit ]; then
    echo -e "#!/bin/sh\n\n\nnpm run check" > .git/hooks/pre-commit
    chmod +x .git/hooks/pre-commit
fi
