## 配置飞书

使用飞书 API 需要先创建自己的应用。在飞书开放平台创建应用并申请相应的权限，然后获取访问凭证来调用 API

### 步骤一：创建并配置应用

1. 登陆 [飞书开发者后台](https://open.feishu.cn/app) https://open.feishu.cn/app

2. 在开发者后台首页，单击 **创建企业自建应用**，填写应用名称、描述以及图标信息，然后单击 **创建**。

   <p align="center">
      <img width="600" src="./public/images/tutorial_飞书1.png" alt="tutorial_飞书1"/>
   </p>

   <p align="center">
      <img width="300" src="./public/images/tutorial_飞书2.png" alt="tutorial_飞书2"/>
   </p>
3. 开通应用权限 只有开通了应用权限，我们才能将我们的账单信息上传到飞书多维表格中

   1. 在应用详情页左侧导航栏，单击 **权限管理**。

   2. 在 **权限配置** 页面左侧列表，单击 **云文档**，找到 **查看、评论、编辑和管理多维表格** 和 **查看、评论和导出多维表格**权限，并在 **操作** 列单击 **开通权限**。

   <p align="center">
      <img width="800" src="./public/images/tutorial_飞书3.png" alt="tutorial_飞书3"/>
   </p>

4. 在弹出的对话框中，点击**确认并前往创建应用版本**

   <p align="center">
      <img width="500" src="./public/images/tutorial_飞书4.png" alt="tutorial_飞书4"/>
   </p>

5. 点击右上角**创建版本** ，进入版本详情页面，填写**应用版本号**和**更新说明**填写完成后拉到最下角点击**保存**

   1. 点击**创建版本**
      
      <p align="center">
         <img width="600" src="./public/images/tutorial_飞书5.png" alt="tutorial_飞书5"/>
      </p>

   3. 填写**应用版本号**和**更新说明**

      <p align="center">
         <img width="600" src="./public/images/tutorial_飞书6.png" alt="tutorial_飞书6"/>
      </p>

   4. 拉到最下边，点击**保存**

      <p align="center">
         <img width="600" src="./public/images/tutorial_飞书7.png" alt="tutorial_飞书7"/>
      </p>

6. 在弹出的对话框中，点击**申请线上发布**

   <p align="center">
      <img width="600" src="./public/images/tutorial_飞书8.png" alt="tutorial_飞书8"/>
   </p>

7. 确认后我们就能看到我们需要的 **App ID** 和 **App Secret** 了，将它们保存下来，我们之后会用到

   <p align="center">
      <img width="800" src="./public/images/tutorial_飞书9.png" alt="tutorial_飞书9"/>
   </p>

### 步骤二：配置飞书多维表格模板

1. 点击飞书链接：https://mq8si4rq2bm.feishu.cn/base/Xuy5bPCHlaKSlrsMKjicNk5En8b?from=from_copylink

2. 点击右下角按钮**使用该模板**
   
   <p align="center">
      <img width="600" src="./public/images/tutorial_表格1.png" alt="tutorial_表格1"/>
   </p>

3. 安装我们在**步骤一**创建好的应用

   1. 点击表格**右上角的三个小圆点**→点击弹出菜单中的**更多**→点击**添加文档应用**
      
      <p align="center">
         <img width="600" src="./public/images/tutorial_表格3.png" alt="tutorial_表格3"/>
      </p>

   2. 在弹出的对话框**输入刚刚创建的应用名**，**点击应用**进行安装
      
      <p align="center">
         <img width="400" src="./public/images/tutorial_表格4.png" alt="tutorial_表格4"/>
      </p>

## 部署API

1. 点击 [链接](https://github.com/Reborn14/Intelligent-Accounting-Assistant/fork)，fork 本项目

2. 注册并登陆 [Render](https://render.com/)，推荐使用 GitHub 登陆

   > Render 是一个国外的云服务提供商，它提供了一系列托管服务，包括静态站点、Web应用程序和无服务器功能。
   
   <p align="center">
      <img width="500" src="./public/images/tutorial_register_render.jpg" alt="tutorial_register_render"/>
   </p>

3. 点击链接创建 [New Web Service (render.com)](https://dashboard.render.com/create?type=web)

4. 选择连接 **Intelligent-Accounting-Assistant**

   <p align="center">
      <img width="600" src="./public/images/tutorial_连接本项目.jpg" alt="tutorial_连接本项目"/>
   </p>

5. 填写**名称**和**启动命令**，并选择**免费**项目

   启动命令：`uvicorn main:app --host 0.0.0.0 --port 10000`

   <p align="center">
      <img width="600" src="./public/images/tutorial_设置名称.jpg" alt="tutorial_设置名称"/>
   </p>
   
   <p align="center">
      <img width="600" src="./public/images/tutorial_填写启动命令.jpg" alt="tutorial_填写启动命令"/>
   </p>

6. 设置环境变量

<div align="center">
   
   | 键(Key)    | 值(Value)                      |
   | ---------- | ------------------------------ |
   | API_KEY    | 自己设置一个`api_key`          |
   | APP_ID     | 填入刚刚创建应用的`app_id`     |
   | APP_SECRET | 填入刚刚创建应用的`app_secret` |
   | APP_TOKEN  | 填入自己表格的`app_token`      |
   | TABLE_ID   | 填入自己表格的`table_id`       |
   
</div>

   <p align="center">
      <img width="800" src="./public/images/tutorial_set_environment.jpg" alt="tutorial_set_environment"/>
   </p>

   > 如何提取表格的 `app_token` 和 `table_id`?
   >
   > 举例：https://mq8si4rq2bm.feishu.cn/base/VWsIbKc2XaPrY6s2H8Tcp1h5nRh?table=tblu6KShUtEAiIa2&view=vewBl0dBVY
   >
   > `app_token` =  VWsIbKc2XaPrY6s2H8Tcp1h5nRh
   >
   > `table_id`= tblu6KShUtEAiIa2

7. 点击创建

## 创建GPTs

1. 点击 [链接](https://github.com/Reborn14/Intelligent-Accounting-Assistant/blob/main/prompt.md)，复制 prompt

   - 替换 prompt 中的 `url` 地址为自己的多维表格
     
   <p align="center">
      <img width="800" src="./public/images/tutorial_替换prompt.jpg" alt="tutorial_替换prompt"/>
   </p>

2. 点击 [链接](https://github.com/Reborn14/Intelligent-Accounting-Assistant/blob/main/howtofilter.json)，下载 knowledge 文件

3. 点击 [链接](https://github.com/Reborn14/Intelligent-Accounting-Assistant/blob/main/openapi.json)， 复制 `OpenAPI schema`

   1. 替换 `url`为自己部署的 `render 地址`

   <p align="center">
      <img width="800" src="./public/images/tutorial_替换openapi.jpg" alt="tutorial_替换openapi"/>
   </p>

   2. 设置 `Authentication` ,填入刚刚设置的 `Api_Key`

   <p align="center">
      <img width="500" src="./public/images/tutorial_填写apikey.jpg" alt="tutorial_填写apikey"/>
   </p>

4. 完成 GPTs 的创建

