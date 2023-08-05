import re
final_text = 'Némo est aveugle : Cependant, elle distingue les êtres vivants ou simplement animés. Pour le reste, elle utilise une cane *(cf [[(Fiche) Mnémosyne#Trivia|trivia]])*'
title="autre fichier"
line = final_text
if re.search(
        '\[{2}(.*)#(.*)]{2}', final_text
        ):  # title working → Convertion for the blog
    # Need to be converted to []() links
    link = re.search('\[{2}(.*)#(.*)]{2}', final_text)
    file_name = re.search('\[{2}(.*)#', final_text)
    file_name = file_name.group().replace('#', '').replace('[', '')
    if file_name == title:
        if re.search('\|', final_text):
            # get headings
            heading = re.search('\|(.*)\]{2}', final_text).group().replace(']', '')

            heading = '[' + heading.replace('|', '') + ']'
        else:
            heading = ""
        # [heading](link !) → #things

        link = re.search('#(.*)(\|)?', link.group())
        if heading == "":
            title = link.group(0).lstrip()
            title = title.replace(']', '')
            title = title.replace('#', '')
            heading = '[' + title + ']'
        link = link.group(1).lower()
        link = re.sub('\|(.*)', '', link)
        section = re.sub('[^ \w\-\d_]', '', link)
        section = section.lstrip()
        section = re.sub('[^\w\d]', '-', section) + '-'
        final_text = heading + '(#' + section + ')'
        final_text = re.sub('\[{2}(.*)\]{2}', final_text, line)
    else:
        head = re.search('#(.*)(\|?)', link.group())
        head = head.group().replace(']', '')
        if not re.search('\|', final_text):
            heading = title + ' ▷ '+ head
            check_head = False
        else:
            info_file = re.sub('\|(.*)', '', head)
            heading = ' ('+ title + ' ▷ '+ info_file.strip() + ')'
            check_head= True
        final_text = re.sub('#(.*)\|', f'\|', line)
        if check_head is False:
            final_text = re.sub(']]', f'\|{heading}]]', final_text)
        else:
            print(heading)
            final_text = re.sub(']]', f'{heading}', final_text)
        print(final_text)


