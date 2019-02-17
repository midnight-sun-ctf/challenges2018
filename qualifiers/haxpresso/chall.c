#include "chall.h"

static porder orders_arr[10] = {0};
static u32 orders_arr_len = 0;
static v0 * current_order = NULL;

v0 banner()
{
	puts("\e[49m          \e[49m\e[38;5;16m▄▄\e[48;5;16m\e[38;5;243m▄\e[48;5;16m\e[38;5;253m▄▄▄▄▄▄▄\e[48;5;16m\e[38;5;252m▄\e[49m\e[38;5;16m▄▄\e[49m        \n\e[0m   " \
	"\e[49m      \e[49m\e[38;5;16m▄\e[48;5;16m\e[38;5;255m▄\e[48;5;250m\e[38;5;231m▄\e[48;5;231m\e[38;5;253m▄\e[48;5;231m\e[38;5;252m▄\e[48;5;252m\e[38;5;255m▄\e[48;5;252m\e[38;5;243m▄\e[48;5;250m\e[38;5;243m▄▄▄\e[48;5;252m\e[38;5;243m▄\e[48;5;252m\e[38;5;255m▄\e[48;5;231m\e[38;5;252m▄\e[48;5;231m\e[38;5;255m▄\e[48;5;253m\e[38;5;231m▄\e[48;5;16m\e[38;5;255m▄\e[49m\e[38;5;16m▄\e[49m      \n\e[0m   " \
	"\e[49m     \e[49m\e[38;5;16m▄\e[48;5;16m\e[38;5;238m▄\e[48;5;231m\e[38;5;253m▄\e[48;5;231m \e[48;5;253m\e[38;5;231m▄\e[48;5;255m\e[38;5;231m▄▄▄▄▄▄▄▄▄\e[48;5;253m\e[38;5;231m▄\e[48;5;255m\e[38;5;231m▄\e[48;5;255m\e[38;5;243m▄\e[48;5;16m\e[38;5;238m▄\e[49m\e[38;5;16m▄\e[49m     \n\e[0m   " \
	"\e[49m   \e[49m\e[38;5;16m▄\e[48;5;16m\e[38;5;231m▄\e[48;5;253m\e[38;5;102m▄\e[48;5;102m\e[38;5;253m▄\e[48;5;231m \e[48;5;253m\e[38;5;231m▄\e[48;5;255m\e[38;5;231m▄\e[48;5;231m\e[38;5;255m▄▄▄\e[48;5;231m\e[38;5;253m▄▄▄▄\e[48;5;255m\e[38;5;252m▄▄\e[48;5;252m\e[38;5;250m▄\e[48;5;248m\e[38;5;250m▄\e[48;5;248m \e[48;5;102m \e[48;5;243m\e[38;5;238m▄\e[48;5;16m\e[38;5;243m▄\e[49m\e[38;5;16m▄\e[49m   \n\e[0m   " \
	"\e[49m   \e[48;5;16m \e[48;5;231m\e[38;5;255m▄\e[48;5;102m\e[38;5;231m▄\e[48;5;253m \e[48;5;253m\e[38;5;255m▄\e[48;5;231m\e[38;5;255m▄▄▄\e[48;5;231m   \e[48;5;255m  \e[48;5;255m\e[38;5;253m▄\e[48;5;253m \e[48;5;253m\e[38;5;252m▄\e[48;5;250m\e[38;5;248m▄▄\e[48;5;248m\e[38;5;246m▄\e[48;5;248m\e[38;5;102m▄\e[48;5;240m\e[38;5;253m▄\e[48;5;253m\e[38;5;250m▄\e[48;5;16m \e[49m   \n\e[0m   " \
	"\e[49m   \e[49m\e[38;5;16m▀\e[49m\e[38;5;250m▀\e[48;5;255m\e[38;5;16m▄\e[48;5;231m\e[38;5;250m▄▄\e[48;5;253m \e[48;5;253m\e[38;5;255m▄\e[48;5;255m \e[48;5;255m\e[38;5;231m▄▄▄\e[48;5;253m\e[38;5;231m▄▄\e[48;5;252m\e[38;5;231m▄▄\e[48;5;250m\e[38;5;253m▄\e[48;5;246m\e[38;5;253m▄▄\e[48;5;250m\e[38;5;102m▄\e[48;5;250m\e[38;5;240m▄\e[48;5;255m\e[38;5;16m▄\e[49m\e[38;5;243m▀\e[49m\e[38;5;16m▀\e[49m   \n\e[0m   " \
	"\e[49m     \e[48;5;16m \e[48;5;255m\e[38;5;253m▄\e[48;5;255m \e[48;5;250m\e[38;5;231m▄\e[48;5;252m\e[38;5;255m▄\e[48;5;252m\e[38;5;253m▄\e[48;5;252m\e[38;5;250m▄\e[48;5;252m\e[38;5;248m▄▄\e[48;5;252m\e[38;5;246m▄▄\e[48;5;250m\e[38;5;246m▄▄▄\e[48;5;246m\e[38;5;248m▄\e[48;5;243m\e[38;5;250m▄\e[48;5;243m\e[38;5;248m▄\e[48;5;102m \e[48;5;16m \e[49m     \n\e[0m   " \
	"\e[49m     \e[48;5;16m \e[48;5;253m\e[38;5;248m▄\e[48;5;255m \e[48;5;231m       \e[48;5;255m  \e[48;5;253m  \e[48;5;250m  \e[48;5;248m \e[48;5;102m \e[48;5;16m \e[49m     \n\e[0m   " \
	"\e[49m      \e[48;5;16m \e[48;5;255m  \e[48;5;231m \e[48;5;231m\e[38;5;255m▄\e[48;5;113m\e[38;5;22m▄\e[48;5;28m\e[38;5;22m▄\e[48;5;22m \e[48;5;22m\e[38;5;248m▄\e[48;5;22m \e[48;5;28m\e[38;5;248m▄\e[48;5;113m\e[38;5;22m▄\e[48;5;253m\e[38;5;65m▄\e[48;5;250m  \e[48;5;248m \e[48;5;16m \e[49m      \n\e[0m   " \
	"\e[49m      \e[48;5;16m \e[48;5;255m\e[38;5;253m▄\e[48;5;255m \e[48;5;253m\e[38;5;250m▄\e[48;5;113m\e[38;5;240m▄\e[48;5;248m\e[38;5;238m▄\e[48;5;240m\e[38;5;102m▄\e[48;5;238m\e[38;5;253m▄\e[48;5;238m\e[38;5;246m▄\e[48;5;238m\e[38;5;231m▄\e[48;5;240m\e[38;5;238m▄\e[48;5;22m\e[38;5;238m▄\e[48;5;22m\e[38;5;240m▄\e[48;5;250m\e[38;5;248m▄\e[48;5;248m \e[48;5;102m \e[48;5;16m \e[49m      \n\e[0m   " \
	"\e[49m      \e[49m\e[38;5;16m▀\e[48;5;252m\e[38;5;16m▄\e[48;5;255m \e[48;5;250m \e[48;5;238m\e[38;5;65m▄\e[48;5;238m\e[38;5;240m▄\e[48;5;250m\e[38;5;238m▄▄\e[48;5;250m\e[38;5;231m▄\e[48;5;250m\e[38;5;253m▄\e[48;5;250m\e[38;5;238m▄\e[48;5;238m\e[38;5;240m▄\e[48;5;243m\e[38;5;22m▄\e[48;5;248m  \e[48;5;102m\e[38;5;16m▄\e[49m\e[38;5;16m▀\e[49m      \n\e[0m   " \
	"\e[49m       \e[48;5;16m \e[48;5;255m \e[48;5;252m\e[38;5;231m▄\e[48;5;113m\e[38;5;255m▄\e[48;5;22m\e[38;5;248m▄\e[48;5;240m\e[38;5;22m▄\e[48;5;231m\e[38;5;22m▄\e[48;5;238m\e[38;5;248m▄\e[48;5;238m\e[38;5;22m▄\e[48;5;240m\e[38;5;248m▄\e[48;5;248m\e[38;5;22m▄\e[48;5;22m\e[38;5;65m▄\e[48;5;250m \e[48;5;248m \e[48;5;16m \e[49m       \n\e[0m   " \
	"\e[49m       \e[48;5;16m \e[48;5;255m\e[38;5;253m▄\e[48;5;231m  \e[48;5;113m\e[38;5;231m▄\e[48;5;28m\e[38;5;231m▄\e[48;5;22m\e[38;5;231m▄\e[48;5;22m\e[38;5;255m▄▄\e[48;5;28m\e[38;5;253m▄\e[48;5;113m\e[38;5;253m▄\e[48;5;252m \e[48;5;250m\e[38;5;248m▄\e[48;5;248m\e[38;5;246m▄\e[48;5;16m \e[49m       \n\e[0m   " \
	"\e[49m       \e[49m\e[38;5;16m▀\e[48;5;253m\e[38;5;16m▄\e[48;5;231m     \e[48;5;255m  \e[48;5;253m  \e[48;5;252m \e[48;5;248m \e[48;5;246m\e[38;5;243m▄\e[49m\e[38;5;16m▀\e[49m       \n\e[0m   " \
	"\e[49m\e[97m	▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄\n\e[0m" \
	"\e[49m\e[97m	▄▄▄▄▄▄ HAXPRESSO ▄▄▄▄▄\n\e[0m");
}

v0 init()
{
  setvbuf(stdout, 0, 2, 0);
  setvbuf(stdin, 0, 2, 0);
}

v0 print_menu()
{
    static u8 menu[] = " \
\nMENU\n \
1) Add order\n \
2) Remove order\n \
3) Checkout order\n \
4) Edit order\n \
5) Quit\n \
> ";
    printf("%s", menu);
}

v0 print_drinks()
{
    static u8 drinks[] = " \
\nMENU\n \
1) $1 Pwn Coffee - 'No cream, just pwn'\n \
2) $2 Jolt Cola - 'The hackers best friend!'\n \
3) $3 Hexpresso - '16 flavours in one drink'\n \
Select drink: ";
    printf("%s", drinks);	
}

u32 get_int()
{
  u8 choice_buf[40] =  "";
  read(0, choice_buf, 40);
  return strtoul(choice_buf, NULL, 0);
}

v0 verify_malloc(v0 * p)
{
  if(p == NULL)
    exit(0);
}

u32 get_answer()
{
  u8 choice_buf[20] =  "";
  read(0, choice_buf, 2);
  if(choice_buf[0] == 'y'){
    return 1;
  }
  return 0;
}

u32 select_drink()
{
  u32 choice = 1;
  while(1){
	 print_drinks();
   choice = get_int();
   if(choice > 0 && choice < 4)
    break;
  }
	return choice;
}

v0 show_current_order(porder * o)
{
  if(o){
    printf("Currently checking out: \n");
    printf("Id: %d\n", ((porder)o)->id);
    printf("Type: %d\n", ((porder)o)->type);
    printf("Price: %d\n", ((porder)o)->price);
    if(((porder)o)->name) {
      printf("Name: %s\n", (u8 *)((porder)o)->name);
    }
  } else {
    printf("Order not found!\n");
  }
}

v0 checkout_order()
{
  u32 cid = 0;
  if(current_order){
    show_current_order(current_order);
    printf("Change order id? (y/n): ");
    if(get_answer()){
      printf("Select order id: ");
      cid = get_int();
      current_order = orders_arr[cid];
    }
  } else {
    printf("Select order id: ");
    cid = get_int();
    current_order = orders_arr[cid];
  }

  if(current_order){
    printf("Finish checking out order id %d? (y/n): ", ((porder)current_order)->id);
    if(get_answer()){
      printf("[\e[32m+\e[0m]Finished checking out id %d!", ((porder)current_order)->id);
      current_order = NULL;
      orders_arr[cid] = NULL;
    }
  } else {
    printf("[\e[31m-\e[0m] Drink order not found!\n");
  }
}

v0 add_order()
{
  u8 name[NAME_MAX_SIZE];

  if(orders_arr_len >= 10){
    printf("[\e[31m-\e[0m] Maximum orders placed!");
    return;
  }

  u32 drink_choice = select_drink();

  orders_arr[orders_arr_len] = malloc(sizeof(order)+1);
  verify_malloc(orders_arr[orders_arr_len]);
  memset(orders_arr[orders_arr_len], 0, sizeof(order)+1);

  orders_arr[orders_arr_len]->id = orders_arr_len;
  orders_arr[orders_arr_len]->type = drink_choice;
  orders_arr[orders_arr_len]->price = drink_choice;
  orders_arr[orders_arr_len]->name = NULL;

  printf("Add name to drink? (y/n): ");
  if(get_answer()){
    printf("Enter name: ");
    read(0, name, NAME_MAX_SIZE);
    orders_arr[orders_arr_len]->name = malloc(strlen(name)+1);
    verify_malloc(orders_arr[orders_arr_len]->name);
    memcpy(orders_arr[orders_arr_len]->name, name, strlen(name));
  }
  orders_arr_len += 1;
  printf("[\e[32m+\e[0m] Drink order added!\n");
}

v0 edit_order()
{
  u8 name[NAME_MAX_SIZE];
  printf("Order id to edit: ");
  u32 i = get_int();
  if(!orders_arr[i]){
    printf("[\e[31m-\e[0m] Drink order not found!\n");
    return;
  }

  if(!orders_arr[i]->name){
    printf("[\e[31m-\e[0m] Drink order has no name to edit!\n");
    return;
  }

  printf("New name for the order: ");
  read(0, name, NAME_MAX_SIZE);
  memcpy(orders_arr[i]->name, name, strlen(name));
  printf("[\e[32m+\e[0m] Order edited!\n");
}


v0 del_order()
{
  printf("Drink order id to remove: ");
  u32 i = get_int();
  if(!orders_arr[i]){
    printf("[\e[31m-\e[0m] Drink order not found!\n");
    return;
  }

  if(orders_arr[i]->name){
    free(orders_arr[i]->name);
  }
  free(orders_arr[i]);
  orders_arr[i] = NULL;
  printf("[\e[32m+\e[0m] Drink order removed!\n");
}

v0 update_firmware()
{
  printf("FIRMWARE UPDATER\nWARNING - AUTHORIZED USERS ONLY!\n");
  printf("Firmware size: ");
  u32 firmware_size = get_int();
  v0 * firmware_data = malloc(firmware_size);
  verify_malloc(firmware_data);

  printf("Firmware data: ");
  read(0, firmware_data, firmware_size);

  printf("Firmware note: ");
  v0 * firmware_note = malloc(100);
  verify_malloc(firmware_note);
  read(0, firmware_note, 99);

  if(strlen(firmware_data) != (firmware_size -1)){
    printf("[\e[31m-\e[0m] Firmware update failed!\n");
    return;
  }
  printf("[\e[32m+\e[0m] Firmware updated successfully!\n");
}

v0 menu()
{
  u32 choice = 0;
  while(1){
      print_menu();
      choice = get_int();
      switch(choice){
          case 0:
            update_firmware();
            break;
          case 1:
          	add_order();
            break;
          case 2:
          	del_order();
            break;
          case 3:
            checkout_order();
            break;
          case 4:
            edit_order();
            break;
          case 5:
            exit(0);
            break;
          default:
            break;
    }
  }
}

u32 main(u32 argc, u8 ** argv)
{
	init();
	banner();
	menu();
}