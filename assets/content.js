// 站点内容文件：改这里就能改网站，不用重新生成。
// 字段含义见仓库 README 的「自己编辑站点内容」一节。
window.SITE_CONTENT = {
  "boot_lines": [
    "> loading operator profile <b>杜凯峰</b> ... ok",
    "> mounting agentharbor ... <b>4013 tests green</b>",
    "> verifying eval set ... <b>60 cases + 6 heldout</b>",
    "> syncing upstream repos ... <b>45 merged PRs</b>",
    "> indexing transmissions ... <b>6 published</b>",
    "> three-track metrics ... 0.932 / 0.830 / 0.550",
    "> all subsystems nominal. welcome, operator."
  ],
  "i18n": {
    "zh": {
      "home.hero.tagline": "AGENT ENGINEER · BACKEND INTERN · OPEN TO WORK",
      "home.hero.title": "用确定性工程",
      "home.hero.highlight": "驯化模型的不确定性。",
      "home.hero.paragraph.0": "三个从零开始的系统：AgentHarbor（自托管多渠道 Agent 工作台）、HFusionHub（双语言多租户 RAG 平台）、Coupon Hub（高并发优惠券营销平台）；同时给 bytedance/deer-flow 累计 45 个已合并 PR。",
      "nav.overview.label": "概览",
      "nav.missions.label": "项目",
      "nav.arsenal.label": "武器库",
      "nav.blog.label": "个人博客",
      "nav.terminal.label": "终端"
    },
    "en": {
      "home.hero.tagline": "AGENT ENGINEER · BACKEND INTERN · OPEN TO WORK",
      "home.hero.title": "Taming model uncertainty with",
      "home.hero.highlight": "deterministic engineering.",
      "home.hero.paragraph.0": "Three systems built from scratch: AgentHarbor (self-hosted multi-channel agent workbench), HFusionHub (dual-language multi-tenant RAG platform), Coupon Hub (high-concurrency coupon platform); plus 45 merged upstream PRs at bytedance/deer-flow.",
      "nav.overview.label": "Overview",
      "nav.missions.label": "Missions",
      "nav.arsenal.label": "Arsenal",
      "nav.blog.label": "Blog",
      "nav.terminal.label": "Terminal"
    }
  },
  "site": {
    "brand": "HFusion",
    "handle": "",
    "initials": ""
  },
  "github": {
    "username": "xiaodu55"
  },
  "home": {
    "hero": {
      "tagline": "AGENT ENGINEER · BACKEND INTERN · OPEN TO WORK",
      "title": "用确定性工程",
      "highlight": "驯化模型的不确定性。",
      "bio": "三个从零开始的系统：AgentHarbor（自托管多渠道 Agent 工作台）、HFusionHub（双语言多租户 RAG 平台）、Coupon Hub（高并发优惠券营销平台）；同时给 bytedance/deer-flow 累计 45 个已合并 PR。",
      "actions": [
        {
          "label": "探索 GitHub",
          "url": "https://github.com/xiaodu55",
          "primary": true
        },
        {
          "label": "读我的博客",
          "url": "blog.html"
        }
      ],
      "paragraphs": [
        "三个从零开始的系统：AgentHarbor（自托管多渠道 Agent 工作台）、HFusionHub（双语言多租户 RAG 平台）、Coupon Hub（高并发优惠券营销平台）；同时给 bytedance/deer-flow 累计 45 个已合并 PR。",
        "我的信条：数字不由我背书，由冻结产物背书——220 例冻结评测集、4013 条用例、三轨指标归因，每一条都能用一条命令复现。"
      ]
    },
    "meta": {},
    "focus": {},
    "highlights": {
      "title": "数据与成果",
      "items": [
        {
          "icon": "⭐",
          "title": "45 个已合并上游 PR",
          "desc": "覆盖 10 个上游项目；deer-flow 单 PR 最长 12 轮 review 全闭环，PII 脱敏中间件已进入现役栈"
        },
        {
          "icon": "🧪",
          "title": "4013 测试全绿 / 60+6 评测",
          "desc": "AgentHarbor：4013 用例全绿；60 例三档回放 + 6 例 held-out 封存集，Bad 全拒绝 0% 放行、Ambiguous 冻结率 100%"
        },
        {
          "icon": "📊",
          "title": "220 例冻结评测集 · 三轨归因",
          "desc": "离线确定性 0.932 / 纯检索直测 0.830 / runtime 0.550，SHA-256 防漂移"
        },
        {
          "icon": "⚡",
          "title": "1000 并发 P95 14ms",
          "desc": "Coupon Hub：Redis Lua 原子预扣 + RocketMQ 异步落库 + Canal 回写，持续 ~2000 QPS、三方对账零超卖"
        }
      ]
    },
    "contact": {}
  },
  "open_source": {},
  "projects": {
    "lede": "三个从零开始的系统，全部可本地演示，口径与仓库对齐。",
    "stack_lede": "技术栈矩阵与经历线",
    "items": [
      {
        "name": "AgentHarbor",
        "code": "TS/SQLite",
        "tags": [
          "Agent 工作台",
          "多渠道",
          "治理"
        ],
        "summary": "自托管多渠道 Agent 工作台：Web / Electron 与七类 IM 接入，治理三牌（心跳自治 · 污点追踪审批 · 委托驱动）、四账本可靠投递、执行安全三道防线（零网络沙箱 / 工具仲裁 fail-closed / 上下文预算熔断）、六类记忆 + 知识飞轮。",
        "metrics": [
          "4013 TESTS GREEN",
          "60+6 EVAL",
          "Bad 0% 放行",
          "Ambiguous 冻结 100%"
        ],
        "points": [
          "心跳自治：open loop 到期自动唤醒，失败重试 cap 3 + 退避 5′/20′",
          "污点追踪：按内容来源定信任级，跨会话外发封存为审批草稿",
          "委托驱动：owner 注册目标 → 机器可判交付判据 → 泵推进 → 刹车三件"
        ]
      },
      {
        "name": "HFusionHub",
        "code": "JAVA+PYTHON",
        "tags": [
          "多租户",
          "RAG",
          "评测门禁"
        ],
        "summary": "双语言多租户 RAG 平台：Java 管写路径（事务 / 租户 / 计费），Python 管 AI 全链路，HMAC 跨语言契约。",
        "metrics": [
          "220 例冻结集",
          "0.932 / 0.830 / 0.550",
          "行锁 120s→ms"
        ],
        "points": [
          "审批 exactly-once：三表同事务 + 一次性 scoped 执行令牌（fail-closed）+ 守卫 UPDATE 幂等迁移",
          "RAG 全链路：意图分类 → 查询分解 DAG → 多路召回（向量 + BM25，RRF）→ 逐论断 [n] 引用溯源",
          "GraphRAG 立项评审：基线满分，数据驱动否决并预先写死复开条件"
        ]
      },
      {
        "name": "Coupon Hub",
        "code": "JAVA 17",
        "tags": [
          "高并发",
          "营销平台"
        ],
        "summary": "高并发优惠券营销平台：Redis Lua 原子预扣 + 布隆过滤 + RocketMQ 异步落库 + Canal binlog 缓存回写。",
        "metrics": [
          "1000 并发 P95 14ms",
          "~2000 QPS",
          "零超卖"
        ],
        "points": [
          "缓存一致性三方案实测：aside / 延迟双删 / binlog 脏读率与窗口",
          "关单双方案：定时消息 vs 死信队列 + timer wheel 拥塞事故复盘",
          "修复基线 3 个真实缺陷"
        ]
      }
    ],
    "stack": {
      "title": "技术栈矩阵",
      "groups": [
        {
          "label": "AGENT",
          "items": [
            "LangGraph 中间件链",
            "MCP 规范",
            "ReAct 与工具审批",
            "治理（心跳 / 污点审批 / 委托）"
          ]
        },
        {
          "label": "RAG / EVAL",
          "items": [
            "向量 + BM25/FTS → RRF",
            "冻结评测套件",
            "三轨指标归因",
            "引用溯源"
          ]
        },
        {
          "label": "BACKEND",
          "items": [
            "Java 17 / Spring Boot 3",
            "Spring Cloud Alibaba",
            "MyBatis Plus / Flyway",
            "条件 UPDATE 状态机"
          ]
        },
        {
          "label": "MIDDLEWARE",
          "items": [
            "Redis（Lua / Redisson / 布隆）",
            "RocketMQ 5（定时消息 / 死信）",
            "MySQL + ShardingSphere",
            "Canal / Elasticsearch"
          ]
        },
        {
          "label": "POLYGLOT",
          "items": [
            "TypeScript / Node（Electron）",
            "Python（FastAPI · 检索管线）",
            "vitest / CI 质量门禁"
          ]
        },
        {
          "label": "CRAFT",
          "items": [
            "证据级提交文化",
            "活体验收",
            "变异复验（热路径确认）",
            "负责任漏洞披露"
          ]
        }
      ]
    },
    "chrono": [
      {
        "period": "2026.07–",
        "title": "AgentHarbor · 核心设计与开发",
        "detail": "治理三牌 + 四账本 + 知识飞轮；Phase 4 RSI 自改进闭环"
      },
      {
        "period": "2026.02–",
        "title": "HFusionHub · 独立设计与开发",
        "detail": "双语言 RAG 平台，220 例冻结评测与三轨归因体系"
      },
      {
        "period": "2025–",
        "title": "Coupon Hub · 独立设计与开发",
        "detail": "高并发优惠券营销平台，Redis Lua 原子预扣 + 布隆 + RocketMQ + Canal"
      }
    ]
  },
  "learning": {
    "lede": "把踩过的坑写成可复现的复盘：先出事故，再讲判据。知乎 / 掘金 / 公众号「小杜手册」三平台同步。",
    "note_short": "PUBLISHED",
    "blog": {
      "title": "掘金 · HFusion",
      "url": "https://juejin.cn/user/1335237353931068"
    },
    "items": [
      {
        "title": "计划没有错，错的就是计划：我给 Agent 装心跳的五次排雷",
        "url": "https://juejin.cn/post/7703384226859909130",
        "date": "2026-11-02",
        "tags": [
          "Agent"
        ],
        "summary": "给 Agent 装心跳调度踩了 5 个坑：计划预设「执行必成功」导致游标误消费、意图静默蒸发。复盘 CAS 撞车、状态解耦、退避重试与单测盲区。",
        "views": 4
      },
      {
        "title": "fail-open 还是 fail-closed？看职责，不凭偏好",
        "url": "https://juejin.cn/post/7700156802533146675",
        "date": "2026-10-25",
        "tags": [
          "后端"
        ],
        "summary": "守卫位（令牌、权限、指纹、时效）一律 fail-closed；增强位（脱敏、证据门控）允许 fail-open。答案出自一张表，不出自性格。",
        "views": 17
      },
      {
        "title": "差点发出去的错数字：从 0.93 到 0.55，我的 RAG 评测为什么必须分三条轨道",
        "url": "https://juejin.cn/post/7699773245550116874",
        "date": "2026-10-24",
        "tags": [
          "RAG"
        ],
        "summary": "先造尺子，再调管线：0.932 不是全链路成绩而是离线确定性轨，轨道标错会让结论整个反转。",
        "views": 25
      },
      {
        "title": "Claude Duet 刷屏：亲手造过一遍的人，怎么看这波“主动式 Agent”",
        "url": "https://juejin.cn/post/7699372774716178442",
        "date": "2026-10-23",
        "tags": [
          "Claude"
        ],
        "summary": "每个转述细节标注信源边界，再用手写过的心跳调度系统逐条对照：哪些一致，哪里选了相反的默认值。",
        "views": 57
      },
      {
        "title": "热门技术当前，我怎么有依据地说“不”",
        "url": "https://juejin.cn/post/7699019490776121407",
        "date": "2026-10-22",
        "tags": [
          "GraphRAG"
        ],
        "summary": "基线怎么测、缺口怎么验尸、「不立项」为什么还要带复开条件——这篇刻意不报数字。",
        "views": 40
      },
      {
        "title": "事务的锁租期：一次 120 秒行锁事故复盘",
        "url": "https://juejin.cn/post/7698799059633537078",
        "date": "2026-10-21",
        "tags": [
          "MySQL"
        ],
        "summary": "读超时 120 秒的 HTTP 调用占满三张表行锁，连接池跟着陪葬：勘查、归因与两刀修法。",
        "views": 43
      }
    ],
    "stats": [
      [
        "已发布",
        "6"
      ],
      [
        "同步平台",
        "3"
      ],
      [
        "最近更新",
        "2026-11-02"
      ]
    ],
    "platforms": "知乎 / 掘金 / 公众号「小杜手册」三平台同步：每篇先出事故现场，再讲判据，最后给可复现的验证方式。",
    "cta": {
      "text": "新文章先在掘金首发，再同步到知乎与公众号「小杜手册」。掘金没有公开的个人 RSS，想订阅可以点开主页关注。",
      "url": "https://juejin.cn/user/1335237353931068"
    }
  },
  "terminal": {
    "lede": "联系方式与常用入口。",
    "lines": [
      {
        "text": "duk@agent-ops:~ — profile shell v1.0"
      },
      {
        "text": "> whoami",
        "tone": "ok"
      },
      {
        "text": "杜凯峰 / DU KAIFENG — AI 应用工程师（Agent 方向）· 全栈开发"
      },
      {
        "text": "> contact",
        "tone": "ok"
      },
      {
        "text": "email   kfeng.du@outlook.com",
        "tone": "warn"
      },
      {
        "text": "wechat  17636153050",
        "tone": "warn"
      },
      {
        "text": "qq      1704788159",
        "tone": "warn"
      },
      {
        "text": "> links",
        "tone": "ok"
      },
      {
        "text": "github  github.com/xiaodu55"
      },
      {
        "text": "juejin  juejin.cn/user/1335237353931068"
      },
      {
        "text": "> status",
        "tone": "ok"
      },
      {
        "text": "OPEN TO WORK — 全职 AI 应用 / Agent 方向，或实习合作",
        "tone": "err"
      }
    ],
    "commands": {
      "help": "可用命令：whoami / status / github / juejin / email / wechat / qq / stats / clear",
      "whoami": "杜凯峰 / DU KAIFENG — AI 应用工程师（Agent 方向）· 全栈开发",
      "status": "OPEN TO WORK — 全职 AI 应用 / Agent 方向，或实习合作",
      "github": "github.com/xiaodu55",
      "juejin": "juejin.cn/user/1335237353931068",
      "email": "kfeng.du@outlook.com",
      "wechat": "17636153050",
      "qq": "1704788159",
      "stats": "merged PRs 45 / upstream 10 repos / tests green 4013 / eval 220 冻结集 + 60 回放"
    }
  }
};
window.SITE_I18N = {
  "zh": {
    "home.hero.tagline": "AGENT ENGINEER · BACKEND INTERN · OPEN TO WORK",
    "home.hero.title": "用确定性工程",
    "home.hero.highlight": "驯化模型的不确定性。",
    "home.hero.paragraph.0": "三个从零开始的系统：AgentHarbor（自托管多渠道 Agent 工作台）、HFusionHub（双语言多租户 RAG 平台）、Coupon Hub（高并发优惠券营销平台）；同时给 bytedance/deer-flow 累计 45 个已合并 PR。",
    "nav.overview.label": "概览",
    "nav.missions.label": "项目",
    "nav.arsenal.label": "武器库",
    "nav.blog.label": "个人博客",
    "nav.terminal.label": "终端"
  },
  "en": {
    "home.hero.tagline": "AGENT ENGINEER · BACKEND INTERN · OPEN TO WORK",
    "home.hero.title": "Taming model uncertainty with",
    "home.hero.highlight": "deterministic engineering.",
    "home.hero.paragraph.0": "Three systems built from scratch: AgentHarbor (self-hosted multi-channel agent workbench), HFusionHub (dual-language multi-tenant RAG platform), Coupon Hub (high-concurrency coupon platform); plus 45 merged upstream PRs at bytedance/deer-flow.",
    "nav.overview.label": "Overview",
    "nav.missions.label": "Missions",
    "nav.arsenal.label": "Arsenal",
    "nav.blog.label": "Blog",
    "nav.terminal.label": "Terminal"
  }
};
