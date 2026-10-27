import type { ReactNode } from "react";
import ReactMarkdown, { type Components } from "react-markdown";
import { Link } from "react-router-dom";
import rehypeRaw from "rehype-raw";
import remarkGfm from "remark-gfm";

/** Join a markdown-relative href onto the document's repo folder. */
function resolveRepoPath(baseDir: string, href: string): string | null {
  if (/^[a-z][a-z0-9+.-]*:/i.test(href) || href.startsWith("#") || href.startsWith("/")) {
    return null;
  }
  const parts = baseDir ? baseDir.split("/") : [];
  for (const segment of href.split("#")[0].split("/")) {
    if (segment === "" || segment === ".") continue;
    if (segment === "..") parts.pop();
    else parts.push(segment);
  }
  return parts.join("/");
}

/** Map a repo path (problems/..., learn/...) to the in-app route that shows it. */
function routeFor(repoPath: string): string | null {
  let match = repoPath.match(/^problems\/(p\d+)-[^/]+(\/README\.md)?$/);
  if (match) return `/p/${match[1]}`;
  match = repoPath.match(/^learn\/\d{2}-[^/]+\/(\d{2})\.(\d+[a-z]?)-[^/]+(\/README\.md)?$/);
  if (match) return `/p/L${match[1]}.${match[2]}`;
  match = repoPath.match(/^learn\/(\d{2})-[^/]+(\/README\.md)?$/);
  if (match) return `/learn/${match[1]}`;
  if (/^learn\/?(README\.md)?$/.test(repoPath)) return "/learn";
  if (/^problems\/?$/.test(repoPath)) return "/";
  return null;
}

/**
 * The hints in each problem README are wrapped in raw
 * `<details><summary>Hint N</summary>` blocks, so rehypeRaw is required - without
 * it the hints would either vanish or render pre-expanded, defeating their point.
 *
 * `baseDir` is the repo-relative folder of the document. With it, relative links
 * between READMEs (lesson -> exercise, exercise -> lesson, lesson -> problems/)
 * become in-app navigation instead of 404s.
 */
export default function MarkdownPane({
  source,
  baseDir = "",
}: {
  source: string;
  baseDir?: string;
}) {
  const components: Components = {
    a: ({ href = "", children }: { href?: string; children?: ReactNode }) => {
      const repoPath = resolveRepoPath(baseDir, href);
      const route = repoPath === null ? null : routeFor(repoPath);
      if (route) return <Link to={route}>{children}</Link>;
      if (/^https?:/i.test(href)) {
        return (
          <a href={href} target="_blank" rel="noreferrer">
            {children}
          </a>
        );
      }
      return <a href={href}>{children}</a>;
    },
  };

  return (
    <div className="markdown">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeRaw]}
        components={components}
      >
        {source}
      </ReactMarkdown>
    </div>
  );
}
