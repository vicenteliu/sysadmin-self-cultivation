# A self-contained image: the documents travel with the viewer.
# Build from the REPO ROOT, because the content is the repo:
#
#   docker build -f site/Dockerfile -t sysadmin-docs .
#   docker run --rm -p 8099:8080 sysadmin-docs
#
# Baking freezes the content. `site/corpus.json` and `docs/index.json` are copied as
# they stand, so regenerate both before building or the search will describe a repo
# that no longer exists:
#
#   python3 docs/build-index.py && python3 site/build-corpus.py
#
FROM nginx:1.27-alpine

COPY site/nginx.conf /etc/nginx/conf.d/default.conf
COPY . /repo

# The image is a viewer, not a workspace: drop everything the contract cannot serve.
RUN rm -rf /repo/.git /repo/.serena /repo/.claude /repo/toolbox/*/__pycache__ \
 && chown -R nginx:nginx /repo

EXPOSE 8080
