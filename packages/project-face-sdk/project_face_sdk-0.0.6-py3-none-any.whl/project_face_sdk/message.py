import json
import os
import datetime
import dateutil.parser

'''
{
  task_id: 1,
  type: '1', //1='日常', 2='临时', 3='视频'
  channel: '',  //频道唯一标识
  video_id: '', //视频的唯一标识
  retry: 0,  //重试次数
  video_url: '',    //视频下载链接
  date: '2021-08-06 12:22:01', //视频开始时间
  end_date: '2021-08-06 12:22:01', //视频结束时间
  video_source: '', //视频拷贝的挂载路径或者视频url
  data_source: ''   //视频来源
  config: { //任务的参数
    fps: 6,                //每秒帧数
    resolution: "800:-1", //图片大小
    person_type_threshold: {
        '1': 0.5,
        '2': 0.4,
    },
  },
  frame_index:500,             //视频帧的序号
  frame_total: 10024,          //视频总帧数，-1表示不能确定
  frame_filename: '',                //图片文件地址
  width: 800,                  //图片宽度
  height: 600,                 //图片高度
  faces:[                   //人脸框，可能有多个人脸
    {
      box:[50, 50, 100, 100],
      persons:[
        [1, '张三', 0.987, 1],  //[人物ID，人物名称，相似度sim，是否正面人物]
        [2, '李四', 0.987, 0],
        [3, '王五', 0.987, 1],
      ]
    }
  ]
}
'''


class Message:
    def __init__(self, message_type, info):
        self.message_type = message_type
        self.info = info

        assert self.message_type in [ 'video_source', 'video', 'framing', 'scan', 'asr'], "message_type 错误"
        assert type(info.get('task_id')) == int, "task_id 格式错误"
        assert info.get('type') in [1, 2, 3], "type 格式错误"
        assert type(info.get('retry')) == int, "retry 格式错误"
        self._str_is_not_empty('channel')
        self._str_is_not_empty('video_id')
        self._str_is_not_empty('channel')
        self._str_is_not_empty('date')
        self._str_is_not_empty('end_date')
        self._str_is_not_empty('video_source')
        self._str_is_not_empty('data_source')

        assert type(info.get('config')) == dict, "config 格式错误"
        assert type(info.get('config').get('resolution')) == str, "resolution 格式错误"
        assert type(info.get('config').get('person_type_threshold')) == dict, "config 格式错误"
        #assert type(info.get('config').get('threshold')) == float, "threshold 格式错误"
        #assert type(info.get('config').get('person_type_ids')) == str, "person_type_ids 格式错误"

        if self.message_type in ['framing', 'scan', 'video', 'asr']:
            self._str_is_not_empty('video_url')

        if self.message_type == 'framing' or self.message_type == 'scan':
            assert type(info.get('frame_index')) == int, "frame_index 格式错误"
            assert type(info.get('frame_total')) == int, "frame_total 格式错误"
            self._str_is_not_empty('frame_filename')

        if self.message_type == 'scan':
            assert type(info.get('width')) == int, "width 格式错误"
            assert type(info.get('height')) == int, "height 格式错误"
            assert type(info.get('faces')) == list and len(
                info.get('faces')) > 0

        if self.message_type == 'asr':
            self._str_is_not_empty('audio_task_id')
            self._str_is_not_empty('audio_filename')
            self._str_is_not_empty('asr_service_ip')

    def _str_is_not_empty(self, name):
        assert type(self.info.get(name)) == str and len(
            self.info.get(name)) > 0, "字符串{}，不能为空".format(name)

    def __getattr__(self, name):
        if name in ['fps', 'resolution']:
            return self.info['config'].get(name)

        if name in self.info:
            return self.info.get(name)
        else:
            raise Exception('{} 未定义'.format(name))

    def get_log_columns(self):
        message = self.info

        columns = []
        columns.append(str(message['task_id']))
        columns.append(str(message['type']))
        columns.append(str(message['channel']))
        columns.append(str(message['video_id']))
        columns.append(str(message['retry']))
        columns.append(str(message['date']))
        columns.append(str(message['end_date']))
        columns.append(str(message['video_source']))
        columns.append(str(message['data_source']))
        columns.append(str(message['config']['fps']))
        columns.append(str(message['config']['resolution']))
        columns.append(str(message['config']['person_type_threshold']))

        if self.message_type in ['framing', 'scan', 'video', 'asr']:
            columns.append(str(message['video_url']))

        if self.message_type == 'framing' or self.message_type == 'scan':
            columns.append(str(message['frame_index']))
            columns.append(str(message['frame_total']))
            columns.append(str(message['frame_filename']))

        if self.message_type == 'scan':
            columns.append(str(message['width']))
            columns.append(str(message['height']))

        if self.message_type == 'asr':
            columns.append(str(message['audio_task_id']))
            columns.append(str(message['audio_filename']))
            columns.append(str(message['asr_service_ip']))

        return columns

    def get_frame_message(self, frame_index, frame_total, frame_filename):
        assert self.message_type == 'video'

        info = self.info
        info['frame_index'] = frame_index
        info['frame_total'] = frame_total
        info['frame_filename'] = frame_filename
        return Message('framing', info)

    def get_scan_message(self, faces, width, height):
        assert self.message_type == 'framing'

        info = self.info
        info['faces'] = faces
        info['width'] = width
        info['height'] = height
        return Message('scan', info)

    def get_path(self, *, is_filename=False):
        info = self.info
        path = self._get_video_uniq('/')

        if is_filename == True:
            return "{}/{}.jpg".format(path, info['frame_index'])
        else:
            return path

    def get_dot_time(self):
        assert self.message_type == 'framing' or self.message_type == 'scan'
        return round(self.info['frame_index']/self.info['config']['fps'], 3)

    def get_frame_play_time(self):
        assert self.message_type == 'framing' or self.message_type == 'scan'

        date = dateutil.parser.parse(self.info['date'])
        return date + datetime.timedelta(seconds=self.get_dot_time())

    def dumps(self):
        return bytes(json.dumps(self.info), encoding="utf8")

    def _get_video_uniq(self, separator='/'):
        return separator.join([
            str(self.info['task_id']),
            self.info['channel'], 
            str(self.info['video_id']), 
            str(self.info['retry'])
        ])

    # 返回视频的唯一标识
    def get_video_uniq_id(self):
        return self._get_video_uniq('-')

    def get_asr_message(self, task_id, audio_filename, asr_service_ip):
        assert self.message_type == 'video'

        info = self.info
        info['audio_task_id'] = task_id
        info['audio_filename'] = audio_filename
        info['asr_service_ip'] = asr_service_ip
        return Message('asr', info)

    def delete_frame(self):
        assert self.message_type=='framing' or self.message_type=='scan'

        os.remove(self.info['frame_filename'])

    def get_video_message(self, video_url):
        assert self.message_type == 'video_source'

        info = self.info
        info['video_url'] = video_url
        return Message('video', info)

    @classmethod
    def loads(cls, step, body):
        return Message(step, json.loads(str(body, encoding='utf-8')))
    
