#include <stdlib.h>
#include <stdio.h>
#include <signal.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h> 
#include <pthread.h>
#include <unistd.h>
#include <alloca.h>

#include "botpanel.h"

#define DATA_SIZE 300

u32 g_timeout = 0;
pthread_attr_t g_thread_attr = {0};
connection g_con[10];
u32 g_con_num = 0;

static u32 trial_mode = 0;

v0 leet_banner()
{

  puts(
"\e[49m                          \e[49m\e[38;5;133m▄\e[48;5;133m\e[38;5;176m▄▄\e[48;5;96m\e[38;5;133m▄\e[49m\e[38;5;96m▄\e[49m                            \n\e[0m " \
"\e[49m                          \e[48;5;176m  \e[48;5;133m\e[38;5;96m▄\e[48;5;133m \e[48;5;133m\e[38;5;96m▄\e[49m\e[38;5;237m▄\e[49m                           \n\e[0m " \
"\e[49m                          \e[48;5;176m\e[38;5;133m▄\e[48;5;133m \e[48;5;96m\e[38;5;133m▄\e[48;5;133m \e[48;5;96m\e[38;5;133m▄\e[48;5;133m \e[48;5;96m\e[38;5;237m▄\e[49m                          \n\e[0m " \
"\e[49m                          \e[49m\e[38;5;96m▀\e[48;5;133m\e[38;5;237m▄\e[48;5;133m  \e[48;5;133m\e[38;5;237m▄\e[48;5;133m  \e[48;5;237m\e[38;5;133m▄\e[49m                         \n\e[0m " \
"\e[49m                               \e[48;5;237m \e[48;5;133m  \e[49m\e[38;5;96m▄\e[49m                        \n\e[0m " \
"\e[49m                                \e[49m\e[38;5;237m▀\e[48;5;133m\e[38;5;237m▄\e[48;5;237m \e[49m                        \n\e[0m " \
"\e[49m                                 \e[48;5;237m \e[48;5;133m \e[48;5;96m\e[38;5;237m▄\e[49m                       \n\e[0m " \
"\e[49m                                  \e[48;5;133m \e[48;5;237m \e[49m                       \n\e[0m " \
"\e[49m                                  \e[48;5;96m \e[48;5;237m \e[49m                       \n\e[0m " \
"\e[49m                                \e[49m\e[38;5;237m▄▄\e[48;5;96m \e[48;5;237m \e[49m                       \n\e[0m " \
"\e[49m                             \e[49m\e[38;5;133m▄\e[48;5;96m\e[38;5;133m▄\e[48;5;133m      \e[48;5;96m\e[38;5;133m▄\e[49m\e[38;5;237m▄\e[49m                    \n\e[0m " \
"\e[49m                   \e[49m\e[38;5;96m▄▄\e[49m      \e[49m\e[38;5;96m▄\e[49m\e[38;5;176m▄\e[48;5;237m \e[48;5;237m\e[38;5;96m▄\e[48;5;133m\e[38;5;237m▄\e[48;5;133m       \e[48;5;237m\e[38;5;133m▄\e[49m\e[38;5;237m▄\e[49m\e[38;5;233m▄\e[49m                 \n\e[0m " \
"\e[49m                  \e[48;5;96m\e[38;5;237m▄\e[48;5;176m\e[38;5;130m▄\e[48;5;133m\e[38;5;237m▄\e[48;5;96m\e[38;5;133m▄\e[49m\e[38;5;133m▄\e[49m \e[49m\e[38;5;133m▄\e[49m\e[38;5;96m▄\e[49m\e[38;5;237m▄\e[48;5;96m\e[38;5;133m▄\e[48;5;176m\e[38;5;96m▄\e[48;5;185m  \e[48;5;237m\e[38;5;133m▄\e[48;5;133m\e[38;5;233m▄\e[48;5;133m       \e[48;5;96m  \e[49m\e[38;5;233m▄\e[49m                \n\e[0m " \
"\e[49m                   \e[48;5;237m \e[48;5;185m \e[48;5;237m\e[38;5;185m▄\e[48;5;133m\e[38;5;96m▄\e[48;5;133m\e[38;5;176m▄\e[48;5;176m  \e[48;5;133m  \e[48;5;96m\e[38;5;133m▄\e[48;5;185m\e[38;5;133m▄\e[48;5;185m \e[48;5;133m \e[48;5;237m \e[48;5;133m    \e[48;5;133m\e[38;5;237m▄\e[48;5;96m  \e[48;5;96m\e[38;5;233m▄\e[48;5;237m \e[48;5;96m\e[38;5;179m▄\e[48;5;233m \e[49m               \n\e[0m " \
"\e[49m                     \e[48;5;96m\e[38;5;237m▄\e[48;5;176m   \e[48;5;176m\e[38;5;133m▄\e[48;5;133m\e[38;5;237m▄\e[48;5;237m\e[38;5;231m▄\e[48;5;96m\e[38;5;252m▄\e[48;5;133m       \e[48;5;133m\e[38;5;223m▄\e[49m\e[38;5;237m▀\e[49m   \e[49m\e[38;5;233m▀▀\e[49m                \n\e[0m " \
"\e[49m                 \e[49m\e[38;5;130m▀\e[48;5;130m\e[38;5;58m▄\e[48;5;130m \e[49m\e[38;5;96m▄\e[48;5;237m\e[38;5;133m▄\e[48;5;133m \e[48;5;176m\e[38;5;133m▄\e[48;5;133m \e[48;5;133m\e[38;5;179m▄\e[48;5;167m\e[38;5;125m▄\e[48;5;231m\e[38;5;179m▄▄\e[48;5;133m\e[38;5;58m▄▄\e[48;5;133m\e[38;5;223m▄▄\e[48;5;58m \e[48;5;58m\e[38;5;133m▄\e[48;5;133m\e[38;5;96m▄\e[48;5;223m\e[38;5;237m▄\e[49m                      \n\e[0m " \
"\e[49m                    \e[48;5;176m\e[38;5;133m▄\e[48;5;133m \e[48;5;133m\e[38;5;237m▄\e[48;5;179m\e[38;5;223m▄\e[48;5;223m \e[48;5;223m\e[38;5;130m▄▄\e[48;5;223m   \e[48;5;223m\e[38;5;58m▄\e[48;5;58m\e[38;5;133m▄▄\e[48;5;133m \e[48;5;133m\e[38;5;237m▄\e[49m\e[38;5;237m▀\e[49m                       \n\e[0m " \
"\e[49m                    \e[48;5;233m\e[38;5;133m▄\e[48;5;223m\e[38;5;233m▄▄\e[48;5;130m\e[38;5;231m▄\e[48;5;231m \e[48;5;240m \e[48;5;233m \e[48;5;125m\e[38;5;167m▄\e[48;5;130m\e[38;5;167m▄\e[48;5;179m \e[48;5;179m\e[38;5;237m▄\e[48;5;133m   \e[49m\e[38;5;233m▀\e[49m                        \n\e[0m " \
"\e[49m                  \e[49m\e[38;5;237m▄\e[48;5;237m\e[38;5;223m▄\e[48;5;133m\e[38;5;223m▄\e[48;5;133m \e[48;5;133m\e[38;5;237m▄\e[49m\e[38;5;233m▀▀\e[49m \e[48;5;179m \e[48;5;167m\e[38;5;130m▄\e[48;5;130m \e[48;5;58m\e[38;5;233m▄\e[48;5;237m\e[38;5;133m▄\e[48;5;133m  \e[48;5;133m\e[38;5;237m▄\e[49m                         \n\e[0m " \
"\e[49m                  \e[49m\e[38;5;237m▀\e[49m\e[38;5;223m▀\e[49m\e[38;5;176m▀\e[49m\e[38;5;237m▀\e[49m    \e[49m\e[38;5;58m▀\e[49m\e[38;5;223m▀▀\e[48;5;237m\e[38;5;223m▄\e[48;5;133m\e[38;5;223m▄▄\e[48;5;96m\e[38;5;233m▄\e[49m\e[38;5;233m▀\e[49m                         \n\e[0m " \
"\e[49m                             \e[48;5;223m\e[38;5;130m▄\e[48;5;179m\e[38;5;223m▄\e[48;5;130m\e[38;5;233m▄\e[49m\e[38;5;233m▀\e[49m                          \n\e[0m " \
"\e[49m                                                           \n\e[0m " \
"\e[49m ▄▄ $1337 SHELLS ▄▄                           ▄▄ $2 CCs! ▄▄                                                  \n\e[0m " \
"\e[49m\e[38;5;237m▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ BOT PANEL LOGIN ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄\n\e[0m");
    
}

v0 show_menu(v0 * f)
{
  static u8 menu_trial[] = "\n\
MENU [\e[31mTRIAL MODE\e[0m]\n \
1) Show available bots\n \
2) Send invite\n \
3) Send feedback\n \
4) Quit\n> ";

  static u8 menu[] = "\n\
MENU [\e[32mREGISTERED MODE\e[0m]\n \
1) Show available bots\n \
2) Send invite\n \
3) Send feedback\n \
4) Quit\n> ";

  if(trial_mode){
    if(f > 0){
      sendstr(((pconnection)f)->fd, menu_trial);
    } else {
      printf("%s", menu_trial);
    }
  } else {
    if(f > 0){
      sendstr(((pconnection)f)->fd, menu);
    } else {
      printf("%s", menu);
    }
  }
}

v0 show_bots(v0 * f){
    static u8 bots[] = "\n\
BOTS LISTING\n \
ID\tSTATUS\t\tPC-NAME\t\tOS\tCOUNTRY\t\tPRICE\n \
1\t[\e[32mONLINE\e[0m]\tADAM-PC\t\twin7\tSWEDEN\t\t$4\n \
2\t[\e[32mONLINE\e[0m]\tERIK-PC\t\twin7\tSWEDEN\t\t$6\n \
3\t[\e[31mOFFLINE\e[0m]\tFRA-PC\t\twin10\tSWEDEN\t\t>>$100 HOT DEAL!<<\n \
4\t[\e[32mONLINE\e[0m]\tJOHAN-PC\twin8\tSWEDEN\t\t$10\n";

  if(f > 0){
    sendstr(((pconnection)f)->fd, bots);
  } else {
     printf("%s", bots);
  }
}

v0 init()
{
  pthread_attr_init(&g_thread_attr);
  if(pthread_attr_setstacksize((pthread_attr_t*)&g_thread_attr, 0x3C000) != 0){
    printf("thread failed\n");
    exit(0);
  }

  setvbuf(stdout, 0, 2, 0);
  setvbuf(stdin, 0, 2, 0);
}

v0 send_invite()
{
  u8 ip[20] = "";
  u8 port[20] = "";
  u32 iport = 0;
  printf("Send an invite to a friendly blackhat!\n");
  printf("IP:");
  read(0, ip, 20);
  printf("\nPort:");
  read(0, port, 20);
  iport = strtoul(port, NULL, 0);
  connectback(ip, iport);
}

u32 get_int(v0 *f)
{
  u32 choice = 0;
  u8 choice_buf[4] =  "";

  recv_until(((pconnection)f)->fd, choice_buf, 4, '\n');
  return strtoul(choice_buf, NULL, 0);  
}

v0 send_feedback(v0 *f)
{
  u8 feedback[52] = "";
  u8 choice_buf[4] = "";
  static u32 len = 0;

  sendstr(((pconnection)f)->fd, "\nFeedback length: ");
  len = get_int(f);
  if(len < 0 || len > 50){
    sendstr(((pconnection)f)->fd, "\nFeedback length is incorrect!\n");
    return;
  }
  sendstr(((pconnection)f)->fd, "\nFeedback: ");
  recv_until(((pconnection)f)->fd, feedback, len, '\n');
  sendstr(((pconnection)f)->fd, "\nEdit feedback y/n?: ");
  recv_until(((pconnection)f)->fd, choice_buf, 2, '\n');
  if(choice_buf[0] == 'y'){
    sendstr(((pconnection)f)->fd, "\nFeedback: ");
    recv_until(((pconnection)f)->fd, feedback, len, '\n');
  }
}

v0 invite_handler(v0 * f)
{
  u32 choice = 0;
  u8 choice_buf[4] =  "";

  while(1){
      memset(choice_buf, 0, 4);
      show_menu(f);
      recv_until(((pconnection)f)->fd, choice_buf, 4, '\n');
      choice = strtoul(choice_buf, NULL, 0);
      switch(choice){
          case 1:
            show_bots(f);
            break;
          case 2:
            sendstr(((pconnection)f)->fd, "Invites not allowed in invite-mode\n");
            break;
          case 3:
            send_feedback(f);
            break;
          case 4:
            close(((pconnection)f)->fd);
            pthread_exit(0);
            break;
          default:
            break;
    }
  }
}

v0 remove_newline(u8 * s)
{
  if(strlen(s) > 1){
    if(s[strlen(s)-1] == '\n'){
      s[strlen(s)-1] = '\0';
    }
  }
}

v0 login(u8 * password, u8 * is_trial)
{
  u32 authenticated = 0;
  u32 attempts = 5;
  u8 msg[12] = "";

  while(!authenticated){
    printf("\n\t\tPanel password: ");
    read(0, msg, 12);
    remove_newline(msg);
    if(strncmp(msg, password, strlen(password)) == 0){
      break;
    }

    attempts--;
    printf("\t\t\e[31mIncorrect!\e[0m %d attempts left\n", attempts);
    printf("\t\tYour attempt was: ");
    printf(msg);

    if(!attempts){
      exit(0);
    }
  }

  if(is_trial[1] == 'T'){
    trial_mode = 1;
  }
}

u32 login_handler() 
{
    u32 choice = 0;
    u8 choice_buf[4] =  "";

    while(1){
        memset(choice_buf, 0, 4);
        show_menu(0);
        read(0, choice_buf, 2);
        choice = strtoul(choice_buf, NULL, 0);
        switch(choice){
            case 1:
              show_bots(0);
              break;
            case 2:
                if(!trial_mode){
                  send_invite();
                } else {
                  printf("Invites not allowed in Trial-mode, send some Bitcoins for full-access!\n");
                }
                break;
            case 3:
              printf("Feedback is only allowed in invite-mode\n");
              break;
            case 4:
                exit(0);
            default:
                break;
        }
    }
    exit(0);
}

u32 main(int argc, u8 * argv[]){
  u8 password[20] = "";
  u8 is_trial[8] = "";
  
  if (argc > 1){
      g_timeout = strtoul(argv[1], NULL, 0);
      if(g_timeout > 0){
        alarm(60);
      }
  }
  else{
    printf("botpanel useage:\n./botpanel <timeout> (>0 = normal, 0 = debug)\n");
    exit(0);
  }

  init();
  leet_banner();

  FILE * f = fopen("./config", "rb");
  if(!f){
    printf("no config file!\n");
    return 0;
  }

  fread(password, 1, 11, f);
  fread(is_trial, 1, 2, f);
  
  login(password, is_trial);
  login_handler();
	return 0;
}