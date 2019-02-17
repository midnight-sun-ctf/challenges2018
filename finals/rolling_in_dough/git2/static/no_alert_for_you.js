/*

        If there is no alert,
        	how can there be XSS?
                      /
                     /
            )            (
           /(   (\___/)  )\
          ( #)  \ ('')| ( #
           ||___c\  > '__||
           ||**** ),_/ **'|
     .__   |'* ___| |___*'|
      \_\  |' (    ~   ,)'|
       ((  |' /(.  '  .)\ |
        \\_|_/ <_ _____> \______________
         /   '-, \   / ,-'      ______  \
b'ger   /      (//   \\)     __/     /   \
                            './_____/

*/
window.alert = (x=>prompt("He confirm. He alert. But most of all he prompt."));