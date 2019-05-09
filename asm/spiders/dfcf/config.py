"""
    configure for spider
"""
# site name for east money web site
SITE = 'dfcf'


# news category
class _NewsCategory:
    def __init__(self, id, name, category, interval):
        self.id, self.name, self.category, self.interval = id, name, category, interval


# 新闻
class news:
    NAME = '新闻'

    # 类别
    categories = [ # (id, name, category id(local news category),spider interval in seconds)
        _NewsCategory(350, '国内经济', 1, 5),
        _NewsCategory(351, '国内经济', 1, 10),
        _NewsCategory(353, '证券要闻', 1, 15),
        _NewsCategory(354, '公司新闻', 1, 20),
        _NewsCategory(355, '产经新闻', 1, 30),
        _NewsCategory(363, '纵深调查', 1, 60),

        _NewsCategory(406, '股市直播', 2, 15),
        _NewsCategory(407, '大盘分析', 2, 20),
        _NewsCategory(408, '板块聚焦', 2, 25),
        _NewsCategory(415, '个股点睛', 2, 30),
        _NewsCategory(421, '行业研究', 2, 60),
        _NewsCategory(478, '公司评级', 2, 120),

        _NewsCategory(512, '期市要闻', 3, 20),
        _NewsCategory(517, '焦点观察', 3, 40),
        _NewsCategory(514, '内盘播报', 3, 60),
        _NewsCategory(515, '外盘速递', 3, 120),
        _NewsCategory(519, '交易提示', 3, 360),
        _NewsCategory(522, '交易知识 ', 3, 720),

        _NewsCategory(129, '外汇新闻 ', 4, 120),
        _NewsCategory(130, '外汇评论 ', 4, 360),
        _NewsCategory(133, '投资技巧 ', 4, 720),

        _NewsCategory(569, '黄金要闻 ', 5, 60),
        _NewsCategory(570, '金市评论 ', 5, 240),
        _NewsCategory(571, '贵金属 ', 5, 360),
        _NewsCategory(572, '黄金饰品 ', 5, 720),
    ]


#快讯
class express:
    NAME = '快讯'

    # 类别
    categories = [ # (id, name, category id(local news category),spider interval in seconds)
        _NewsCategory(102, '快讯,7*24', 1, 20),

        _NewsCategory(101, '快讯,要闻', 2, 30),

        _NewsCategory(103, '快讯,上市公司', 3, 40),
        _NewsCategory(104, '快讯,股市直播', 3, 50),
        _NewsCategory(105, '快讯,全球股市', 3, 60),

        _NewsCategory(107, '快讯,外汇', 4, 70),

        _NewsCategory(106, '快讯,商品', 5, 80),

        _NewsCategory(108, '快讯,债券', 6, 90),

        _NewsCategory(109, '快讯,基金', 7, 100),

        _NewsCategory(110, '快讯,地区,中国', 8, 120),
        _NewsCategory(111, '快讯,地区,美国', 8, 130),
        _NewsCategory(112, '快讯,地区,欧洲', 8, 140),
        _NewsCategory(113, '快讯,地区,英国', 8, 150),
        _NewsCategory(114, '快讯,地区,日本', 8, 160),
        _NewsCategory(115, '快讯,地区,加拿大', 8, 170),
        _NewsCategory(116, '快讯,地区,澳洲', 8, 180),
        _NewsCategory(117, '快讯,地区,新兴市场', 8, 190),

        _NewsCategory(118, '快讯,央行,中国', 9, 220),
        _NewsCategory(119, '快讯,央行,美国', 9, 230),
        _NewsCategory(120, '快讯,央行,欧洲', 9, 240),
        _NewsCategory(121, '快讯,央行,英国', 9, 250),
        _NewsCategory(122, '快讯,央行,日本', 9, 260),
        _NewsCategory(123, '快讯,央行,加拿大', 9, 270),
        _NewsCategory(124, '快讯,央行,澳洲', 9, 280),

        _NewsCategory(125, '快讯,数据,中国', 10, 320),
        _NewsCategory(126, '快讯,数据,美国', 10, 330),
        _NewsCategory(127, '快讯,数据,欧洲', 10, 340),
        _NewsCategory(128, '快讯,数据,英国', 10, 350),
        _NewsCategory(129, '快讯,数据,日本', 10, 360),
        _NewsCategory(130, '快讯,数据,加拿大', 10, 370),
        _NewsCategory(131, '快讯,数据,澳洲', 10, 380),
    ]
