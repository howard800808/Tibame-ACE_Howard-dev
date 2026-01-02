graph TD

%% 定義樣式

classDef client fill:#e1f5fe,stroke:#01579b,stroke-width:2px;

classDef entry fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;

classDef mvc fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;

classDef ai fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;

classDef db fill:#e0e0e0,stroke:#616161,stroke-width:2px;



subgraph Client_Side [客戶端層]

Browser[瀏覽器 Web / Dashboard]:::client

LineApp[LINE App / Flex Message]:::client

ExtAPI[外部 API 調用者]:::client

end



subgraph Entry_Layer [入口與路由層]

FastAPI[FastAPI App / Router]:::entry

Auth[OAuth2.0 JWT 驗證]:::entry

WebHook[LINE Webhook Handler]:::entry

end



subgraph Business_Logic [後端核心邏輯 (MVC)]

direction TB


subgraph Controllers [控制器層 (Controllers)]

AuthCtrl[Auth Controller]:::mvc

UserCtrl[User Controller]:::mvc

MBTICtrl[MBTI Controller]:::mvc

LineCtrl[LINE Bot Controller]:::mvc

VideoCtrl[Video Controller]:::mvc

TaskCtrl[Task Controller]:::mvc

LLMCtrl[LLM Controller]:::mvc

McpCtrl[MCP Controller]:::mvc

end



subgraph Services [服務層 (Services)]

UserService[User Service]:::mvc

LineService[Line Bot Service v3]:::mvc

VideoService[Video Service]:::mvc

MBTIService[MBTI Service v3]:::mvc

TaskService[Task Service]:::mvc

EmotionService[Emotion Service]:::mvc

AzureService[Azure Transcription Service]:::mvc

LLMService[Gemini3Pro_ Service]:::mvc

McpService[fastapi_MCP Service]:::mvc

end



subgraph Data_Layer [資料與模型層]

Models[SQLAlchemy & MongoDB Models]:::mvc

Schemas[Pydantic Schemas]:::mvc

Views[Jinja2 Views / HTML]:::mvc

end

end



subgraph External_Services [外部 AI 與雲端服務]

Gemini[Gemini 3 Pro LLM <br/>(MBTI分析)]:::ai

McpPlatform[LLM +MCP <br/>(LLM任務生成)]:::ai

AWS[AWS Rekognition<br/>(情緒分析)]:::ai

Azure[Azure Speech SDK<br/>(STT & 語者分離)]:::ai

LinePlatform[LINE Platform<br/>(Messaging API)]:::ai

end



subgraph Database_Layer [資料持久層]

DB[(Database<br/>SQLite/MySQL)]:::db

DB[(Database<br/>MongoDB)]:::db

end



%% 連線關係

Browser -->|HTTP Request / Token| FastAPI

ExtAPI -->|JSON Request| FastAPI

LLM_ChatAPI -->|JSON Request| FastAPI

LineApp -->|Event Webhook| WebHook

FastAPI --> Auth

WebHook --> LineCtrl

Auth -.->|驗證通過| Controllers



%% Controller 調用

AuthCtrl --> UserService

LineCtrl --> LineService

MBTICtrl --> MBTIService

VideoCtrl --> VideoService

TaskCtrl --> TaskService

LLMCtrl --> LLMService

MCPCtrl --> MCPService



%% Service 邏輯

VideoService --> EmotionService

VideoService --> AzureService

LLMService --> MCPService


%% AI 整合

EmotionService -->|Boto3 SDK| AWS

AzureService -->|Cognitive SDK| Azure

LineService -->|Reply/Push| LinePlatform

MBTIService -->|Google-genai SDK| Gemini 3 Pro

LLMService -->|Google-genai SDK| Gemini 3 Pro

MCPService -->|fastapi_mcp SDK| MCP



%% 資料庫交互

Services --> Models

Models --> DB



%% 視圖渲染

Controllers -->|Data| Views

Views -->|HTML| Browser

Controllers -->|JSON| ExtAPI