#include "duktape/src-custom/duktape.h"
#include "duktape/extras/console/duk_console.h"
#include "curl/include/curl/curl.h"

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/stat.h> 
#include <fcntl.h>
#include <string.h>

#include <sys/types.h>
#include <sys/socket.h>

typedef void v0;
typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;

struct url_data {
    size_t size;
    char* data;
};

v0 verify_malloc(v0 * p)
{
  if(p == NULL)
    exit(0);
}

u32 _read(u8 * buf, u32 len)
{
  return read(0, buf, len);  
}

u32 _write(u8 * buf, u32 len)
{
  return write(1, buf, len);  
}

v0 _write_str(u8 * buf)
{
  _write(buf, strlen(buf));
}

u32 read_int()
{
  u8 choice_buf[40] =  "";
  _read(choice_buf, 40);
  return strtoul(choice_buf, NULL, 0);
}

u32 read_answer()
{
  u8 choice_buf[20] =  "";
  _read(choice_buf, 2);
  if(choice_buf[0] == 'y'){
    return 1;
  }
  return 0;
}

v0 init()
{
  setvbuf(stdout, 0, 2, 0);
  setvbuf(stdin, 0, 2, 0);
}

v0 banner()
{
  puts("\e[49m       \e[49m\e[38;5;239m▄▄▄▄▄▄\e[49m      \n\e[0m " \
"\e[49m    \e[49m\e[38;5;239m▄\e[48;5;239m    \e[48;5;239m\e[38;5;107m▄\e[48;5;239m \e[48;5;239m\e[38;5;237m▄\e[48;5;239m   \e[49m\e[38;5;239m▄\e[49m   \n\e[0m " \
"\e[49m  \e[49m\e[38;5;239m▄\e[48;5;239m     \e[48;5;239m\e[38;5;230m▄\e[48;5;107m\e[38;5;230m▄\e[48;5;107m\e[38;5;60m▄\e[48;5;237m\e[38;5;60m▄\e[48;5;237m \e[48;5;239m\e[38;5;237m▄\e[48;5;239m   \e[49m\e[38;5;239m▄\e[49m \n\e[0m " \
"\e[49m \e[49m\e[38;5;239m▄\e[48;5;239m     \e[48;5;239m\e[38;5;230m▄\e[48;5;230m  \e[48;5;60m  \e[48;5;237m\e[38;5;60m▄\e[48;5;237m  \e[48;5;239m\e[38;5;237m▄\e[48;5;239m  \e[49m\e[38;5;239m▄\n\e[0m " \
"\e[49m \e[48;5;239m    \e[48;5;239m\e[38;5;230m▄\e[48;5;230m \e[48;5;230m\e[38;5;254m▄\e[48;5;254m  \e[48;5;60m    \e[48;5;237m\e[38;5;60m▄\e[48;5;237m  \e[48;5;239m\e[38;5;237m▄\e[48;5;239m \n\e[0m " \
"\e[49m \e[48;5;239m   \e[48;5;230m  \e[48;5;254m \e[48;5;254m\e[38;5;187m▄\e[48;5;187m \e[48;5;187m\e[38;5;250m▄\e[48;5;60m      \e[48;5;237m   \n\e[0m " \
"\e[49m \e[49m\e[38;5;239m▀\e[48;5;239m  \e[48;5;230m \e[48;5;254m\e[38;5;230m▄\e[48;5;254m \e[48;5;187m \e[48;5;250m  \e[48;5;60m      \e[48;5;237m  \e[49m\e[38;5;237m▀\n\e[0m " \
"\e[49m  \e[49m\e[38;5;239m▀\e[48;5;239m \e[48;5;230m\e[38;5;239m▄\e[48;5;230m \e[48;5;254m\e[38;5;230m▄\e[48;5;254m \e[48;5;187m\e[38;5;254m▄\e[48;5;187m \e[48;5;60m     \e[48;5;60m\e[38;5;237m▄\e[48;5;237m \e[49m\e[38;5;237m▀\e[49m \n\e[0m " \
"\e[49m    \e[49m\e[38;5;239m▀\e[48;5;239m \e[48;5;230m\e[38;5;239m▄\e[48;5;230m \e[48;5;254m\e[38;5;230m▄▄\e[48;5;60m   \e[48;5;60m\e[38;5;237m▄\e[48;5;237m \e[49m\e[38;5;237m▀\e[49m   \n\e[0m " \
"\e[49m       \e[49m\e[38;5;239m▀\e[49m\e[38;5;237m▀▀▀▀▀\e[49m      \n\e[0m " \
"\nONION BROWSER");
}

static void my_fatal(void *udata, const char *msg) {
  (void) udata;
  fprintf(stderr, "*** FATAL ERROR: %s\n", (msg ? msg : "no message"));
  fflush(stderr);
  exit(0);
}

void run_js(u8 * script)
{
  void *my_udata = (void *) 0xdeadbeef;
  duk_context *ctx = duk_create_heap(NULL, NULL, NULL, my_udata, my_fatal);
  if(ctx)
  {
    _write_str("#### ANALYSING JAVASCRIPT ####\n");
    duk_console_init(ctx, 0);
    if(duk_peval_lstring(ctx, script, strlen(script)) != 0)
    {
      printf("Analysis failed, exiting! %s\n", duk_safe_to_string(ctx, -1));
      exit(0);
    } 
    _write_str("#### ANALYSIS DONE - SEEMS OK! ####\n");
    duk_destroy_heap(ctx);
  }
}

u32 is_js(u8 * url)
{
  if(strlen(url) > 4 && !strcmp(url + strlen(url) - 3, ".js"))
    return 1;
  return 0;
}

u32 is_html(u8 * url)
{
  if(strlen(url) > 6 && !strcmp(url + strlen(url) - 5, ".html"))
    return 1;
  return 0;
}

size_t write_cb(void *ptr, size_t size, size_t nmemb, struct url_data *data) {
    size_t index = data->size;
    size_t n = (size * nmemb);
    char* tmp;

    data->size += (size * nmemb);

#ifdef DEBUG
    fprintf(stderr, "data at %p size=%ld nmemb=%ld\n", ptr, size, nmemb);
#endif
    tmp = realloc(data->data, data->size + 1); /* +1 for '\0' */

    if(tmp) {
        data->data = tmp;
    } else {
        if(data->data) {
            free(data->data);
        }
        fprintf(stderr, "Failed to allocate memory.\n");
        return 0;
    }

    memcpy((data->data + index), ptr, n);
    data->data[data->size] = '\0';

    return size * nmemb;
}

v0 visit_url(u8 * url)
{
  CURL *curl = NULL;
  CURLcode res = 0;

  if(!is_js(url) && !is_html(url))
  {
    _write_str("[500] - Sorry, that url looks dangerous!\n");
    return;
  }

  curl = curl_easy_init();
  if(curl)
  {
    struct url_data data;
    data.size = 0;
    data.data = malloc(4096); 
    memset(data.data, 0, 4096);

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_NOPROGRESS, 0L);
    curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_cb);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &data);
    res = curl_easy_perform(curl);

    if(res == CURLE_OK)
    {
      if(is_js(url))
      {
        run_js(data.data);
      }
      else if(is_html)
      {
        _write_str("\nView content?: ");
        if(read_answer())
          printf("%s\n", data.data);
      }
    }

    if(data.data)
      free(data.data);
    curl_easy_cleanup(curl);
  }
}

v0 print_menu()
{
  banner();
  _write_str("1) Browse the DARKNET\n2) Exit - I'm not 1337 enough for this\n> ");
}

v0 browser()
{
  static u8 url[200] = "";
  u32 choice = 0;

  while(1)
  {
    print_menu();
    choice = read_int();
    switch(choice)
    {
        case 1:
          memset(url, 0, 200);
          _write_str("Enter url: ");
          _read(url, 200);
          if(url[strlen(url)-1] == '\n')
            url[strlen(url)-1] = '\0';
          visit_url(url);
          break;
        case 2:
          exit(0);
          break;
        default:
          break;
    }
  }
}

int main(int argc, char ** argv)
{
  init();
  browser();
	return 0;
}