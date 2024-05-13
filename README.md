## 概要
Python、OpenTelemetry、Google Cloud Observability でテレメトリーデータを可視化するためのリポジトリです。
Web フレームワークは FastAPI を利用しています。

![Cloud Trace](https://github.com/hayashit6239/react-training/assets/138541920/50a06d7e-2a14-471c-9bbe-8d97cdbf7ddf)

## 環境とコード
Google Cloud Console から起動できる Cloud Shell で動かすことを想定しています。

サンプルコードは Fast API で構成されたアプリケーションに計装する形にしています。
https://github.com/hayashit6239/fastapi-otel-cloudobservability-sample

こちらのリポジトリのコードに関する詳細な内容はこちらの[記事]()を参照ください。

サンプルコードのベースは、SaitoTsutomu さんのコードを引用させていただいています。
https://github.com/SaitoTsutomu/fastapi-book-sample

こちらのコードに関する詳細な内容はこちらの[記事](https://qiita.com/SaitoTsutomu/items/6fd5cd835a4b904a5a3e)を参照ください。

## アプリ と Otel Collector の起動
下記の手順で Cloud Shell 上に FastAPI を用いた Web アプリケーションと Otel Collector を起動します。

※ Cloud Shell 上で起動する都合上、Otel Collector で ADC を無理やり使っている形になっているので気の進まない方は Cloud Run などにデプロイしてください。

```shell:terminal
# リポジトリのクローン
git clone git@github.com:hayashit6239/fastapi-otel-cloudobservability-sample.git

# ADC を使った認証
gcloud auth application-default login

# 保存ディレクトリを書き換えて実行
cd fastapi-otel-cloudobservability-sample && \
cp /tmp/[保存ディレクトリ]/application_default_credentials.json ./containers/otel-collector/application_default_credentials.json && \
chmod 644 ./containers/otel-collector/application_default_credentials.json
```

Otel Collector の設定ファイルである otel-collector.yml の Google Cloud Exporter のプロジェクト ID を修正します。

```yaml:./containers/otel-collector/otel-collector.yml
receivers:
  otlp:
    protocols:
      grpc:

processors:
  batch: {}
  resourcedetection:
    detectors: [env, gcp]
    timeout: 20s
    override: false

exporters:
  debug:
    verbosity: detailed
  googlecloud:
    log:
      default_log_name: opentelemetry.io/collector-exported-log
    project: [project id]

service:
  pipelines:
    metrics:
      receivers: [otlp]
      processors: [batch, resourcedetection]
      exporters: [debug, googlecloud]
    logs:
      receivers: [otlp]
      processors: [batch, resourcedetection]
      exporters: [debug, googlecloud]
    traces:
      receivers: [otlp]
      processors: [batch, resourcedetection]
      exporters: [debug, googlecloud]
```

最後にコンテナのビルドと立ち上げコマンドを実行します。

```shell:terminal
docker compose -f docker-compose.yml build
docker compose -f docker-compose.yml up
```

## FastAPI の挙動を Swagger で確認
Cloud Shell のウェブでプレビュー機能を利用します、ポートを 8000 に変更して「ポート 8000 でプレビュー」をクリックします。別ブラウザが立ち上がるので、`https://8000-**.cloudshell.dev/` となっている URL を `https://8000-**.cloudshell.dev/docs` で Swagger を起動します。

![Swagger](https://github.com/hayashit6239/react-training/assets/138541920/6a8edbea-8716-429a-a723-fd12da3280c3)

Swagger が起動できれば、あとは計装済みである Get Authors や Get Books を叩いて Google Cloud Observability で可視化したり、別の関数に追加の実装して遊んでみてください。