# npbNewsAPI
- 日付、球団、選手を引数に打席結果を返すAPI
- ニュースサイトからスクレイピングしてデータを拝借
- アクセス回数を減らすために、同じパラメーターの場合、キャッシュした結果を用いる
- CloudFunctionにデプロイして公開、データソースにFireStoreを用いる

(イメージ図)
![hoge](https://cdn-ak.f.st-hatena.com/images/fotolife/t/tsk110/20201113/20201113081832.png)

## Usage
### CloudFunctionへのデプロイ
`$ cd functions`

`$ gcloud functions deploy get_data --runtime python38 --trigger-http --allow-unauthenticated`