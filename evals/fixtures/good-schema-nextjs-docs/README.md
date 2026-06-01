# my-docs

A modern documentation framework for JavaScript projects.

Tired of wrestling with clunky docs tools? my-docs gives you beautiful, fast, MDX-powered documentation in 3 commands. Built on Next.js 14, with full-text search, dark mode, and zero-config deployment.

## When to use

- Open-source libraries that need polished docs
- Internal tools documentation
- API reference sites

## When NOT to use

- Simple README-only projects
- Non-technical content (use a CMS instead)

## Install

```bash
npm install -D my-docs
npx my-docs init
npm run docs:dev
```

## FAQ

### Q: Does it support MDX?
A: Yes, full MDX support out of the box.

### Q: Can I deploy to Vercel?
A: Yes, zero-config Vercel deployment.

### Q: Is it free?
A: Yes, MIT licensed, free for commercial use.

### Q: Does it support i18n?
A: Yes, with built-in i18n routing.

### Q: How does it compare to Docusaurus?
A: my-docs is built on Next.js (better DX), has faster builds, and a smaller bundle.

### Q: Can I customize the theme?
A: Yes, fully themeable with Tailwind.

### Q: Does it support versioned docs?
A: Yes, via the `versions.json` config.

### Q: Is there a plugin system?
A: Yes, see the plugin docs.

## Examples

```jsx
import { MyDocs } from 'my-docs';

export default function App() {
  return <MyDocs config={{ theme: 'dark' }} />;
}
```

## License

MIT
