from qqai import SceneR

APPID = "2126903099"
APPKey = "MJLlwhPmkSKbVbtY"

robot = SceneR(APPID, APPKey)

# 识别图片URL
result = robot.run('https://yyb.gtimg.com/aiplat/ai/assets/ai-demo/express-6.jpg')
print(result)
# {'ret': 0, 'msg': 'ok', 'data': {'text': '一位男士在海边骑自行车的照片'}}

# 识别打开的本地图片
with open('/Users/adhcczhang/Desktop/codes/webscrap/img/2_472_0_0.jpg', 'rb') as image_file:
    result = robot.run(image_file)
    print(result)
# {'ret': 0, 'msg': 'ok', 'data': {'text': '一艘飞船'}}
