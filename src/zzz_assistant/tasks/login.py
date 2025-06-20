import os
import time


from src.zzz_assistant.tasks.base_task import BaseTask
from src.zzz_assistant.utils.helpers import wait_for_template
from src.zzz_assistant.utils.paths import ASSETS_PATH


class LoginTask(BaseTask):
    """
    执行登录游戏到主界面的任务
    继承了BaseTask，所以自动拥有了self.device和self.config
    """

    def run(self) -> bool:
        """
        重写run方法，实现登录的具体逻辑
        """
        print("开始执行【登录任务】...")
        # 1. 打开游戏
        game_package_name = self.config['game']['package_name']
        if not game_package_name:
            print("Error: 配置文件未指定游戏包名。")
            return False

        if not self.device.is_game_running(game_package_name):
            print("Warning: 游戏不在前台，尝试开始启动...")
            self.device.start_game(game_package_name)


        # 2. 寻找并点击登录按钮
        login_button_path = os.path.join(ASSETS_PATH, 'login', 'CLICK_INTO_GAME.png')
        login_button_location = wait_for_template(
            self.device,
            login_button_path,
            timeout=120.0)
        if not login_button_location:
            print("Error: 2分钟仍未在截图中找到登录按钮。")
            return False
        # 第一次往往不可点击，会读条，但也不一定
        time.sleep(20)
        print("尝试多等一会...")

        login_button_location = wait_for_template(
            self.device,
            login_button_path,
            timeout=120.0)
        if not login_button_location:
            print("Error: 2分钟仍未在截图中找到登录按钮。")
            return False

        self.device.click(login_button_location[0], login_button_location[1])
        print("已点击登录按钮，等待进入主界面...")


        # 3. 检查该版本是否有广告，若有，等待广告标志出现
        ad_enabled = False
        if self.config['ad']['enabled']:
            ad_enabled = True
            print("该版本有广告弹窗，等待检测并关闭")

        if ad_enabled:
            ad_path = os.path.join(ASSETS_PATH, 'login', '_TEMP_AD_BUTTON.png')
            ad_button_location = wait_for_template(
                self.device,
                ad_path,
                timeout=60.0,
                debug_mode=True)

            if ad_button_location:
                self.device.click(ad_button_location[0], ad_button_location[1])
                print("已点击广告按钮，等待广告关闭...")


        # 4. 等待主界面标志出现
        guide_button_path = os.path.join(ASSETS_PATH, "main_page", "MAIN_GOTO_GUIDE.png")
        guide_button_location = wait_for_template(
            self.device,
            guide_button_path,
            timeout=60.0,
            debug_mode=True)

        if not guide_button_location:
            print("Error: 未在截图中找到主界面标志（目前暂时以是否找到交互按钮为区分）。")
            return False
        print("已进入主界面，【登录任务】完成。")
        return True



