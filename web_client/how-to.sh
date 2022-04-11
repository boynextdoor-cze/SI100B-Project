sudo apt-get install npm
npm update

# Method 1:
# 直接在前端跑起来调试，优点：即时更新，有调试信息；缺点：没法和后端通信
npm run serve

# Method 2:
# 构建前端程序，并输出到web_server中，优点：可以与后端通信；缺点：慢，没有调试信息
./build_client.sh
python3 ../main-test.py

