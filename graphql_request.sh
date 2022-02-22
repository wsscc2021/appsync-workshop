#!/bin/bash
# init
API_URL=""
API_ID=""
API_KEY=""

# createPost
for i in $(seq 1 100); do
    title="the post ${i}"
    content=$(openssl rand -base64 12)
    MUTATION='mutation createPost($input: createPostInput!) { createPost(input: $input) { id, title, content, author, createdAt } }'
    VARIABLES="{\"input\":{\"title\":\"${title}\",\"content\":\"${content}\"}}"
    curl -s -XPOST -H "Content-Type: application/graphql" -H "x-api-key:$API_KEY" -d '{"query": "'"$MUTATION"'","variables": '$VARIABLES'}' $API_URL
done

# getPost
QUERY='query getPost($id: ID!) { getPost(id: $id) { id, title, content, author, createdAt } }'
VARIABLES='{"id":""}'
curl -s -XPOST -H "Content-Type: application/graphql" -H "x-api-key:$API_KEY" -d '{"query": "'"$QUERY"'","variables": '$VARIABLES'}' $API_URL

# listPost
QUERY='query listPost { listPost { id, title, content, author, createdAt } }'
curl -s -XPOST -H "Content-Type: application/graphql" -H "x-api-key:$API_KEY" -d '{"query": "'"$QUERY"'"}' $API_URL

# createComment
postid=""
for i in $(seq 1 100); do
    comment="The comment ${i}"
    MUTATION='mutation createComment($input: createCommentInput!) { createComment(input: $input) { postId, commentId, comment, author, createdAt } }'
    VARIABLES="{\"input\":{\"postId\":\"${postid}\",\"comment\":\"${comment}\"}}"
    curl -s -XPOST -H "Content-Type: application/graphql" -H "x-api-key:$API_KEY" -d '{"query": "'"$MUTATION"'","variables": '$VARIABLES'}' $API_URL
done

# listComment
postid=""
QUERY='query listComment($postId: String!) { listComment(postId: $postId) { postId, commentId, comment, author, createdAt } }'
VARIABLES="{\"postId\":\"${postid}\"}"
curl -s -XPOST -H "Content-Type: application/graphql" -H "x-api-key:$API_KEY" -d '{"query": "'"$QUERY"'","variables": '$VARIABLES'}' $API_URL