import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import remarkGfm from "remark-gfm";

/**
 * The hints in each problem README are wrapped in raw
 * `<details><summary>Hint N</summary>` blocks, so rehypeRaw is required - without
 * it the hints would either vanish or render pre-expanded, defeating their point.
 */
export default function MarkdownPane({ source }: { source: string }) {
  return (
    <div className="markdown">
      <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeRaw]}>
        {source}
      </ReactMarkdown>
    </div>
  );
}
