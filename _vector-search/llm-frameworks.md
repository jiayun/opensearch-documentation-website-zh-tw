---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "LLM 框架整合"
nav_order: 75
---

# LLM 框架整合

數個熱門的大型語言模型 (LLM) 框架可與 OpenSearch 整合作為向量儲存庫，讓您建置可用於正式環境的生成式 AI 應用程式。這些框架提供處理 LLM 的高階抽象層與工具，而其 OpenSearch 整合可讓您使用 OpenSearch 進行高效率的向量儲存、擷取與相似度搜尋：

- LangChain 
    - [語意快取](https://python.langchain.com/docs/integrations/llm_caching/#opensearch-semantic-cache)
    - [向量儲存庫支援](https://pypi.org/project/langchain-opensearch/)
 
- LlamaIndex
    - [向量儲存庫支援](https://developers.llamaindex.ai/python/framework-api-reference/storage/vector_store/opensearch/)
 
- FlowiseAI: 
    - [向量儲存庫支援](https://docs.flowiseai.com/integrations/langchain/vector-stores/opensearch)
 
- Langflow: 
    - [向量儲存庫支援](https://docs.langflow.org/components-vector-stores#opensearch)
 
- Haystack:  
    - [向量儲存庫支援](https://haystack.deepset.ai/integrations/opensearch-document-store)