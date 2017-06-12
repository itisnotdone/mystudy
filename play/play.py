from ptpython.repl import embed
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, shutil
import signal
import time
import readchar
import ast
from util import check_dir, want_to_redo, record, encode_all_in_one, string_handler
from multiprocessing import Process
import json

options = webdriver.ChromeOptions()
options.add_argument("--disable-infobars")
options.add_argument("--verbose")
options.add_argument("--log-path=debug.log")
caps = options.to_capabilities()

driver = webdriver.Remote(
    command_executor='http://127.0.0.1:4444/wd/hub',
    desired_capabilities=caps
)

def get_element(type, location):
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((type, location)))
    return element

def is_clickable(type, location):
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((type, location)))
    return element

def check_point():
    thetime = ''
    while thetime == '':
        theele = get_element(By.XPATH, '//*[@id="video-container"]')
        ActionChains(driver).move_to_element(theele).perform()
        thetime = driver.find_element_by_xpath('//*[@id="currenttime-control"]').text.encode('utf-8')
        time.sleep(0.5)
    current_point = thetime.split('/')[0].strip()
    total_point = thetime.split('/')[1].strip()
    return { 'cp': current_point, 'tp': total_point }

def turn_off_auto_play():
    thetime = ''
    while thetime == '':
        theele = get_element(By.XPATH, '//*[@id="video-container"]')
        ActionChains(driver).move_to_element(theele).perform()
        thetime = driver.find_element_by_xpath('//*[@id="currenttime-control"]').text.encode('utf-8')
    get_element(By.XPATH, '//*[@id="settings"]').click()
    get_element(By.XPATH, '//*[@id="autoplay-off"]').click()
    ActionChains(driver).move_to_element(theele).perform()

def playing():
    if 'Pause' in get_element(
        By.XPATH, '//*[@id="play-control"]').get_attribute('title').encode('utf-8'):
        return True
    else:
        return False

def terminate_recording(proc, file):
    print "Restarting recoding with new layout..."
    proc.terminate()
    time.sleep(2)
    proc.terminate()
    time.sleep(2)
    print 'Deleting the file to start over...'
    os.remove(file)

with open('env.json') as data_file:
    env = json.load(data_file)

driver.set_window_size(800,800)
driver.set_window_position(0,0)
driver.maximize_window()

driver.get(env['main_url'].encode('utf-8') + "/id?redirectTo=/")
print 'Logging..'
get_element(By.ID, 'Username').send_keys(env['user_name'].encode('utf-8'))
get_element(By.ID, 'Password').send_keys(env['user_password'].encode('utf-8'))
get_element(By.ID, 'login').click()


keeping = False
temp_dir = env['temporary_dir'].encode('utf-8')
temp_prefix = temp_dir+'/rMD-session-'
workdir = env['working_dir'].encode('utf-8')

global autoplay
autoplay = True

def start_recording():
    satisfied = False
    new_layout = {
        'xx': env['new_layout']['xx'].encode('utf-8'),
        'yy': env['new_layout']['yy'].encode('utf-8'),
        'wid': env['new_layout']['wid'].encode('utf-8'),
        'hei': env['new_layout']['hei'].encode('utf-8')
    }
    old_layout = {
        'xx': env['old_layout']['xx'].encode('utf-8'),
        'yy': env['old_layout']['yy'].encode('utf-8'),
        'wid': env['old_layout']['wid'].encode('utf-8'),
        'hei': env['old_layout']['hei'].encode('utf-8')
    }

    thetitle = get_element(By.XPATH, '//*[@id="ps-main"]/div/div/section/div[1]/div[2]/h1').text
    is_clickable(By.XPATH, '//*[@id="ps-main"]/div/div/section/div[1]/div[2]/a').click()

    while True:
        if WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2)):
            driver.switch_to_window(driver.window_handles[1])
            break

    if not skip:
        print "< Please turn off auto-play function and do stuffs!!! >"
        embed(globals(), locals())


    ele = get_element(By.XPATH, '//*[@id="tab-table-of-contents"]')
    for sec_idx, sec_val in enumerate(ele.find_elements_by_tag_name('section')):
        if 'open' not in sec_val.get_attribute('class').encode('utf-8'):
            sec_val.click()

        for hea in sec_val.find_elements_by_tag_name('header'):
            for thediv in hea.find_elements_by_css_selector('div.pr-lg.py-md.side-menu-module-title'):
                for theh2 in thediv.find_elements_by_tag_name('h2'):
                    print 'series is '+theh2.text+'.'
                    time.sleep(1)

        for ul in sec_val.find_elements_by_tag_name('ul'):
            for li_idx, li_val in enumerate(ul.find_elements_by_tag_name('li')):
                for theh3 in li_val.find_elements_by_tag_name('h3'):
                    title = string_handler(thetitle)
                    series_num = str(sec_idx + 1).zfill(2)
                    series = string_handler(theh2.text)
                    episode_num = str(li_idx + 1).zfill(2)
                    episode = string_handler(theh3.text)

                    store_dir = workdir+'/'+title
                    check_dir(store_dir)
                    file=series_num+'_'+series+'__'+episode_num+'_'+episode+'.ogv'
                    file_path=store_dir+'/'+file
                    print 'Index is '+str(li_idx)+'...'
                    iseven = li_idx % 2 == 0

                    if os.path.isfile(file_path):
                        print file_path+" is already existing..."
                        continue

                    while True:
                        theh3.click()
                        if playing():
                            ActionChains(driver).key_down(Keys.SPACE).perform()

                        while check_point()['cp'] != '0:00':
                            ActionChains(driver).key_down(Keys.LEFT).perform()

                        global autoplay
                        if autoplay:
                            turn_off_auto_play()
                            autoplay = False

                        print "Getting started to record!"
                        print store_dir
                        print file
                        recoder = record(temp_dir, file_path, new_layout)
                        recoder_pid = recoder.pid

                        if satisfied or skip:
                            break

                        while not satisfied and not skip:
                            print "Are you satisfied with the layout? 'y' or 'n'"
                            input_satisfied = readchar.readchar()
                            if input_satisfied == 'y':
                                satisfied = True
                                terminate_recording(recoder, file_path)
                                break
                            elif input_satisfied == 'n':
                                satisfied = False
                                terminate_recording(recoder, file_path)
                                print 'Please choose a new layout among followings.'
                                print 'New(Default) layout: "'+str(new_layout)+'".'
                                print 'Old layout: "'+str(old_layout)+'".'
                                other_layout = input()
                                new_layout = ast.literal_eval(other_layout)
                                break
                            else:
                                print "Invalid input was entered."

                    print "Playing..."
                    if not playing():
                        ActionChains(driver).key_down(Keys.SPACE).perform()

                    while True:
                        time.sleep(3)
                        if not playing():
                            if check_point()['cp'] == check_point()['tp']:
                                print "finalizing recording..."
                                print "Terminating.."
                                recoder.terminate()
                                time.sleep(3)
                                print "Killing.."
                                recoder.kill()
                                time.sleep(2)
                                print "Deleting.."
                                os.remove(file_path)

                                if iseven:
                                    file_tag = 'done-2'
                                else:
                                    file_tag = 'done-1'

                                os.rename(temp_prefix+str(recoder_pid), temp_prefix+str(recoder_pid)+'-'+file_tag)

                                print ''
                                break

    print 'Finishing recording for this course...!'
    return True

def cleaning_pool():
    for k, v in encoding_pool.items():
        print ''
        print 'Cleaning pool...'
        state = v['proc'].poll()
        if os.path.isfile(v['file']):
            current_size = os.path.getsize(v['file'])
        else:
            print v['file']+' does not exist yet.'

        if state == 0:
            print v['file']+' has been done.'
            print 'Deleting '+temp_prefix+str(k)+'...'
            shutil.rmtree(temp_prefix+str(k))
            del encoding_pool[k]
        else:
            print str(k)+' returned '+str(type(state))+' '+str(state)+'...'
            v['size'] = current_size
        print ''

def keep_recording():
    while True:
        global keeping
        print "Do you want to keep recoding? 'y' or 'n'"
        input_keep_recording = readchar.readchar()
        if input_keep_recording == 'y':
            keeping = True
            break
        elif input_keep_recording == 'n':
            keeping = False
            break
        else:
            print 'Invalid input was entered.'

if os.environ['SKIP']:
    skip = eval(os.environ['SKIP'])
else:
    skip = False

while True:
    if not skip:
        keep_recording()
        embed(globals(), locals())

    if keeping or skip:
        driver.get(env['main_url'].encode('utf-8') + "/library/bookmarks")
        bookmarks_list = get_element(By.XPATH, '//*[@id="ps-main"]/div/main/div/div[2]/div[1]/table/tbody')

        print 'Finding first one from bookmarks_list...'
        first_one = bookmarks_list.find_elements_by_tag_name('tr')[0]
        for idx_sec, val_sec in enumerate(first_one.find_elements_by_class_name('tableTitleCell---1xFo4')):
            for idx_thi, val_thi in enumerate(val_sec.find_elements_by_class_name('displayName---21lBp')):
                being_recorded = val_thi.text
                val_thi.click()

        theresult = start_recording()

        time.sleep(2)

        print 'Cleaning previous window...'
        driver.close()
        print 'Switching back to first window...'
        driver.switch_to_window(driver.window_handles[0])

        print 'Deleting finished course...'
        if theresult:
            print 'Going to bookmark page...'
            driver.get(env['main_url'].encode('utf-8') + "/library/bookmarks")
            print 'Getting bookmark elements...'
            bookmarks_list = get_element(By.XPATH, '//*[@id="ps-main"]/div/main/div/div[2]/div[1]/table/tbody')
            print 'Starting to find the one being recorded...'
            for idx_fir, val_fir in enumerate(bookmarks_list.find_elements_by_tag_name('tr')):
                todelete = False
                for idx_sec, val_sec in enumerate(val_fir.find_elements_by_class_name('tableTitleCell---1xFo4')):
                    for idx_thi, val_thi in enumerate(val_sec.find_elements_by_class_name('displayName---21lBp')):
                        if val_thi.text == being_recorded:
                            todelete = True

                if todelete:
                    for idx_sec, val_sec in enumerate(val_fir.find_elements_by_class_name('tableDeleteCell---2w8zz')):
                        for idx_thi, val_thi in enumerate(val_sec.find_elements_by_class_name('ellipses---3DexB')):
                            val_thi.click()
                            time.sleep(1)
                        for idx_thi, val_thi in enumerate(val_sec.find_elements_by_link_text('Remove Bookmark')):
                            val_thi.click()

        time.sleep(3)

    elif not keeping:
        break


