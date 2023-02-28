import time
import json
from jinja2 import Template
from automaticTestingFramework.conf import env_conf
import shutil
import plotly as py
import chart_studio
from chart_studio.plotly import image
import plotly.graph_objs as go


class Reporter(object):
    """
    report生成器
    """
    def __init__(self, project=None, start=None, duration=None, report_name=None, type=None, generate_result=None):
        self.project = project
        self.start = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start))
        self.duration = duration
        self.template = env_conf.REPORT_TEMPLATE_PATH
        self.mail_template = env_conf.MAIL_TEMPLATE_PATH
        self.generate_result = generate_result
        self.case_info = self._statistic_case_info()
        now = time.strftime("%Y-%m-%d-%H%M%S", time.localtime(time.time()))
        self.report_prefix = "test_report" + now
        if report_name is None:
            self.report_name = self._make_report_name()
        else:
            self.report_name = report_name
        self.type = type
        self.r = None

    def _make_report_name(self):

        report_name = self.report_prefix + ".html"
        return report_name

    def _read_template(self):
        with open(self.template, 'r', encoding='UTF-8') as f:
            t = f.read()
            tp = Template(t)
            self.r = tp.render(project_name=self.project,
                               start_time=self.start,
                               duration_time=self.duration,
                               pass_num=self.case_info.get('pass_num'),
                               all_message=self.generate_result,
                               case_num=self.case_info.get('case_num'),
                               fail_num=self.case_info.get('fail_num'),
                               # fail_messages=self._get_failure_message(),
                               error_num=self.case_info.get('err_num'))
        return self.r

    def _read_mail_template(self):
        with open(self.mail_template, 'r', encoding='UTF-8') as f:
            t = f.read()
            tp = Template(t)
            type_img_url = self.gen_err_img()[0]
            bar_img_url = self.gen_err_img()[1]
            self.r = tp.render(online_report=env_conf.REPORT_SAVED_PATH + self.report_name,
                               start_time=self.start,
                               duration_time=self.duration,
                               pass_num=self.case_info.get('pass_num'),
                               case_num=self.case_info.get('case_num'),
                               fail_num=self.case_info.get('fail_num'),
                               error_num=self.case_info.get('err_num'),
                               type_img=type_img_url,
                               bar_img=bar_img_url)
        return self.r

    def _new_report(self):
        with open(env_conf.REPORT_SAVED_PATH + self.report_name, 'w', encoding="utf8") as f:
            f.write(self.r)
        # 复制当前报告到最新目录
        new_report = env_conf.REPORT_NEWEST_PATH
        shutil.copyfile(env_conf.REPORT_SAVED_PATH + self.report_name, new_report)
    def _new_mail_report(self):
        with open(env_conf.MAIL_REPORT_PATH + self.report_name, 'w', encoding="utf8") as f:
            f.write(self.r)

    def _is_report(self):
        pass

    def _report(self):
        if self.report_name.endswith(self.type):
            self._read_template()
            self._new_report()
        else:
            print("当前生成的报告非指定格式{}".format(self.type))

    def _mail_report(self):
        if self.report_name.endswith(self.type):
            self._read_mail_template()
            self._new_mail_report()
        else:
            print("当前生成的报告非指定格式{}".format(self.type))

    # 统计case执行情况
    def _statistic_case_info(self):
        case_num = len(self.generate_result)
        pass_num = 0
        fail_num = 0
        err_num = 0
        for case in self.generate_result:
            if case['result'] is True:
                pass_num += 1
            elif case['result'] is False:
                fail_num += 1
            else:
                err_num += 1

        case_info = {"case_num": case_num, 'pass_num': pass_num, 'fail_num': fail_num, 'err_num': err_num}
        return case_info

    # 统计所有case总和
    def _count_all(self):
        return len(self.generate_result)

    # 统计成功的case总和
    def _count_success(self):
        return len([s for s in self.generate_result if s['result'] is True])

    # 统计失败的case总和
    def _count_failure(self):
        return len([f for f in self.generate_result if f['result'] is False])

    # 展示所有的case记录
    def _get_all_message(self):
        return [f for f in self.generate_result]

    # 获取失败的case记录
    def _get_failure_message(self):
        return [f for f in self.generate_result if f['result'] is False]

    def _count_error_cases(self):
        return len([s['id'] for s in self.generate_result if s['message'] == "error"])

    def _error_cases(self):
        return [s for s in self.generate_result if s['message'] == "error"]

    # 生成错误类型图
    def gen_err_img(self):
        # 复制最新的报告到newest目录

        # 最新报告截图，与报告同名
        email_path = env_conf.MAIL_REPORT_PATH
        email_img_path = env_conf.MAIL_IMG_PATH
        email_report = email_path + 'report.html'
        pie_image_name = email_img_path + self.report_prefix + '_errorTypes.png'
        bar_image_name = email_img_path + self.report_prefix + '_errorSites.png'

        # 在线认证   username='lijunxian', api_key='2NFfzX94kT8YvH6DEIxC'
        chart_studio.tools.set_credentials_file(username='dushundong', api_key='0qcGMvctzulWscuhYUY8')
        # 使用plotly离线生成图表
        pyplt = py.offline.plot
        # 生成错误类型饼图
        pie_labels = ['success', 'fail', 'error']

        label_values = []
        for key, value in self.case_info.items():
            if key == 'pass_num':
                label_values.append(value)
            elif key == 'fail_num':
                label_values.append(value)
            elif key == 'err_num':
                label_values.append(value)

        pie_trace = [go.Pie(labels=pie_labels, values=label_values)]
        pie_layout = go.Layout(title='Error type distribution',
                               width=600,
                               height=600,
                               margin={'l': 20, 'r': 20, 't': 30, 'b': 10})
        pie_fig = go.Figure(data=pie_trace, layout=pie_layout)
        image.save_as(pie_fig, filename=pie_image_name)

        # 生成错误站点柱状图
        bar_trace = go.Bar(x=pie_labels,
                           y=label_values,
                           text=label_values,
                           textposition='auto',
                           width=0.6)
        data = [bar_trace]
        bar_layout = go.Layout(title='Site with errors',
                               xaxis_tickangle=-45,
                               width=900,
                               height=600,
                               xaxis={'categoryorder': 'category ascending'},
                               margin={'l': 40, 'r': 30, 't': 30, 'b': 35})
        bar_fig = go.Figure(data=data, layout=bar_layout)
        image.save_as(bar_fig, filename=bar_image_name)

        return pie_image_name, bar_image_name


class HtmlReporter(Reporter):
    def __init__(self, project=None, start=None, duration=None, report_name=None, type="html", test_results=None):
        super(HtmlReporter, self).__init__(project, start, duration, report_name, type, test_results)

    def report(self):
        self._report()


class EmailReporter(Reporter):
    def __init__(self, project=None, start=None, duration=None, report_name=None, type="html", test_results=None):
        super(EmailReporter, self).__init__(project, start, duration, report_name, type, test_results)

    def report(self):
        self._mail_report()
