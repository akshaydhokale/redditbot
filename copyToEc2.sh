scp -r -i ~/aws/StockSymbolBotLinux-KeyPair.pem src/*.py $1:~/redditbot/src
scp -r -i ~/aws/StockSymbolBotLinux-KeyPair.pem executebot.sh $1:~/redditbot
