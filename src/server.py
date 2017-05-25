# -*- coding:utf-8 -*-
import BaseHTTPServer
import json
import com.bbd.protonplan.algorithm.entity.Weibo
import time
import math
import

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    '''处理请求并返回页面'''

    # 页面模板
    Page = '''\
    <html>
    <body>
    <table>
    <tr>  <td>Header</td>         <td>Value</td>          </tr>
    <tr>  <td>Date and time</td>  <td>{date_time}</td>    </tr>
    <tr>  <td>Client host</td>    <td>{client_host}</td>  </tr>
    <tr>  <td>Client port</td>    <td>{client_port}</td> </tr>
    <tr>  <td>Command</td>        <td>{command}</td>      </tr>
    <tr>  <td>Path</td>           <td>{path}</td>         </tr>
    </table>
    </body>
    </html>
    '''

    # 处理一个GET请求
    def do_GET(self):
        page = self.create_page()
        self.send_content(page)

    def do_POST(self):
        content_len = int(self.headers.getheader('content-length'))
        post_body = self.rfile.read(content_len)
        self.send_response(200)
        self.end_headers()
        data = json.loads(post_body)
        res = self.calculate_val(data['pubtime'],data['repostscount'],data['commentscount'],data['attitudescount'],data['crawltime_current'],data['repostscount_current'],data['commentscount_current'],data['attitudescount_current'])
        self.wfile.write(res)

    def calculate_val(pubtime,repostscount, commentscount,attitudescount, crawltime_current, repostscount_current, commentscount_current , attitudescount_current):
        res = 0
        hot_score = 0
        try:
            diff_time = (crawltime_current - pubtime) / (60 * 1000)
            hot_score = 0.3 * (0.4 * math.log(repostscount_current / diff_time + 1) + 0.4 * math.log(commentscount_current / diff_time + 1)
            + 0.2 * math.log(attitudescount_current / diff_time + 1))
            + 0.7 * (0.4 * math.log(repostscount_current - repostscount+ 1) + 0.4 * math.log(commentscount_current - commentscount + 1)
            + 0.2 * math.log(attitudescount_current - attitudescount + 1))
            res = '{0: .3g}'.format(hot_score)
        except :
                print("calcHotVal error, hot_score: "+hot_score+"  pubtime: "+pubtime+" repostscount: "+repostscount+" commentscount: "+commentscount+" attitudescount:"+attitudescount+" crawltime_current: "+crawltime_current+" repostscount_current: "+repostscount_current+" commentscount_current: "+commentscount_current+" attitudescount_current: "+attitudescount_current)
        return res


    def send_content(self, page):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(self.path)

    def create_page(self):
        values = {
            'date_time': self.date_time_string(),
            'client_host': self.client_address[0],
            'client_port': self.client_address[1],
            'command': self.command,
            'path': self.path
        }
        page = self.Page.format(**values)
        return page


# ----------------------------------------------------------------------

if __name__ == '__main__':
    serverAddress = ('', 8080)
    server = BaseHTTPServer.HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()
