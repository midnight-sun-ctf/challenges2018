#include "router.h"

void send_output(char * out)
{
	write(STDOUT_FILENO, out, strlen(out));
	write(STDOUT_FILENO, "\n", 1);
}

void send_output_nonl(char * out)
{
	write(STDOUT_FILENO, out, strlen(out));
}

void exit_with_err(char * out)
{
	send_output(out);
	exit(0);
}

void send_success_response(char * page, size_t page_size)
{
	char response_success[MAX_RESP_LEN] = "";
	
	sprintf(response_success, "%s%s%s%d%s%s%s", 
		REQUEST_OK,
		HEADER_SERVER,
		HEADER_CONTENT_LEN,
		page_size,
		HEADER_LINE_END,
		HEADER_END,
		page
		);
	
	send_output(response_success);
}

void send_redirect_response()
{
	char response_redir[512] = "";

	sprintf(response_redir, "%s%s%s%s", 
	REQUEST_REDIR,
	HEADER_LOCATION,
	HEADER_SERVER,
	HEADER_END
	);

	send_output(response_redir);
}

void send_error_response(char * resp_err)
{
	char response_error[MAX_RESP_LEN] = "";

	sprintf(response_error, "%s%s%s%d%s%s", 
	resp_err,
	HEADER_SERVER,
	HEADER_CONTENT_LEN,
	20488,
	HEADER_LINE_END,
	HEADER_END
	);

	load_resource("error.html", response_error+strlen(response_error));
	send_output(response_error);
}

int load_resource(char * res_name, char * filedata)
{
	FILE * fp = NULL;
	long filesize = 0;
	size_t res = 0;

	fp = fopen(res_name, "rb");
	if (!fp)
		return 0;
	
	fseek(fp, 0, SEEK_END);
	filesize = ftell(fp);
	rewind(fp);
	printf("%d", filesize);
	fread(filedata, 1, filesize, fp);
	fclose(fp);
	return 1;
}

void build_page(char * page, char * html)
{
	memcpy(page+strlen(page), html, strlen(html));
}

void url_handler(char * request)
{
	static char data[MAX_RESP_LEN] = "";
	memset(data, 0, MAX_RESP_LEN);

	if (memcmp(request, "GET", 3) != 0 && memcmp(request, "POST", 4) != 0 )
		return send_error_response(REQUEST_BAD);
	
	if (memcmp(request, "GET / ", 6) == 0)
	{
		send_redirect_response();
	}

	if (memcmp(request, "GET /page?=info ", 16) == 0)
	{
		load_resource("html/info.html", data);
		return send_success_response(data, strlen(data));
	}

	if (memcmp(request, "GET /page?=conf ", 16) == 0)
	{
		load_resource("html/conf.html", data);
		return send_success_response(data, strlen(data));
	}

	if (memcmp(request, "GET /page?=admin ", 17) == 0)
	{
		load_resource("html/admin.html", data);
		return send_success_response(data, strlen(data));
	}
	
	if (memcmp(request, "POST /page?=conf ", 17) == 0)
	{
		post_handler(request);
		load_resource("html/conf-success.html", data);
		return send_success_response(data, strlen(data));
	}

	if (memcmp(request, "POST /page?=admin ", 18) == 0)
	{
		load_resource("html/admin-fail.html", data);
		return send_success_response(data, strlen(data));
	}

	return send_error_response(REQUEST_NOT_FOUND);
}

void post_handler(char * request)
{
	static const char conf_file_name [] = "httpd.conf";
	static char fname[255] = "";
	static char zipfile[512];

	char conf_file[512] = "";
	mz_zip_archive archive = {};

	int fname_size = 0;
	int f_index = 0;
	
	if(!parse_post_data(request, zipfile))
	{
		printf("no archive found\n");
		return send_error_response(REQUEST_ERROR);
	}

	if(!mz_zip_reader_init_mem(&archive, zipfile, 512,  MZ_ZIP_FLAG_IGNORE_PATH | MZ_ZIP_FLAG_COMPRESSED_DATA ))
	{
		printf("corrupt archive or larger than 512bytes\n");
		return send_error_response(REQUEST_ERROR);
	}

	if (archive.m_total_files < 1)
	{
		printf("no files in archive?\n");
		return send_error_response(REQUEST_ERROR);
	}

	for (f_index = 0; f_index < archive.m_total_files; f_index++)
	{
		memset(fname, 0, 255);
	    fname_size = mz_zip_reader_get_filename(&archive, f_index, fname, 255);
		if(memcmp(conf_file_name, fname, fname_size) == 0)
		{
			printf("found config, extracting\n");
			mz_zip_reader_extract_to_mem_no_alloc(&archive, f_index, conf_file, 512, NULL, NULL, 0);
			break;
		}
	}
}

int parse_post_data(char * request, char * post_data)
{
	int count = 0;
	char * res =  NULL;

	for (count = 0; count <= MAX_MESSAGE_LEN; count++)
	{
		if(memcmp((char*)request+count, "Content-Type: application\/zip\r\n\r\n", strlen("Content-Type: application\/zip\r\n\r\n")) == 0)
		{
			res = request+count;
			break;
		}
	}

	if(res == NULL)
		return 0;

	memcpy(post_data, res+strlen("Content-Type: application\/zip\r\n\r\n"), 512);
	return 1;
}

void recv_input(char * recv_buffer, int recv_buffer_len)
{
	char input [MAX_MESSAGE_LEN] = "";
	memset(recv_buffer, 0, recv_buffer_len);

	read(STDIN_FILENO, input, MAX_MESSAGE_LEN);
	memcpy(recv_buffer, input, recv_buffer_len);
}

int main()
{
	static char request[MAX_MESSAGE_LEN] = ""; 
	printf("Starting 1337router..\n");
	chdir("/home/ctf/");

	recv_input(request, MAX_MESSAGE_LEN);
	url_handler(request);
	return 0;
}