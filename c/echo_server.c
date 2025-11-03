#include <sys/epoll.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>

#define MAX_EVENTS 64
#define PORT 8080

// 设置非阻塞
void set_nonblocking(int fd) {
    int flags = fcntl(fd, F_GETFL, 0);
    fcntl(fd, F_SETFL, flags | O_NONBLOCK);
}

int main() {
    // 1. 创建监听socket
    int listen_fd = socket(AF_INET, SOCK_STREAM, 0);
    set_nonblocking(listen_fd);
    
    // 设置地址重用
    int opt = 1;
    setsockopt(listen_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
    
    // 绑定地址
    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(PORT);
    
    bind(listen_fd, (struct sockaddr*)&addr, sizeof(addr));
    listen(listen_fd, 128);
    
    // 2. 创建epoll
    int epfd = epoll_create1(0);
    
    // 3. 添加监听socket到epoll
    struct epoll_event ev;
    ev.events = EPOLLIN;
    ev.data.fd = listen_fd;
    epoll_ctl(epfd, EPOLL_CTL_ADD, listen_fd, &ev);
    
    printf("服务器启动在端口 %d\n", PORT);
    
    // 4. 事件循环
    struct epoll_event events[MAX_EVENTS];
    
    while (1) {
        int nfds = epoll_wait(epfd, events, MAX_EVENTS, -1);
        
        for (int i = 0; i < nfds; i++) {
            int fd = events[i].data.fd;
            
            // 新连接
            if (fd == listen_fd) {
                struct sockaddr_in client_addr;
                socklen_t len = sizeof(client_addr);
                
                int client_fd = accept(listen_fd, 
                    (struct sockaddr*)&client_addr, &len);
                
                if (client_fd == -1) {
                    perror("accept");
                    continue;
                }
                
                set_nonblocking(client_fd);
                
                // 添加客户端fd到epoll
                ev.events = EPOLLIN | EPOLLET;  // 边缘触发
                ev.data.fd = client_fd;
                epoll_ctl(epfd, EPOLL_CTL_ADD, client_fd, &ev);
                
                printf("新连接: fd=%d\n", client_fd);
            }
            // 客户端数据
            else {
                char buf[1024];
                
                while (1) {
                    ssize_t n = read(fd, buf, sizeof(buf));
                    
                    if (n > 0) {
                        // Echo回去
                        write(fd, buf, n);
                        printf("Echo %zd bytes to fd=%d\n", n, fd);
                    } else if (n == 0) {
                        // 连接关闭
                        printf("连接关闭: fd=%d\n", fd);
                        epoll_ctl(epfd, EPOLL_CTL_DEL, fd, NULL);
                        close(fd);
                        break;
                    } else {
                        if (errno == EAGAIN) {
                            // 数据读完了
                            break;
                        }
                        perror("read");
                        close(fd);
                        break;
                    }
                }
            }
        }
    }
    
    close(listen_fd);
    close(epfd);
    return 0;
}

