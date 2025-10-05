import React from 'react';
import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import Link from '@tiptap/extension-link';
import Image from '@tiptap/extension-image';
import TextAlign from '@tiptap/extension-text-align';
import EditorToolbar from './EditorToolbar';

const TextEditor = ({ content, onChange, placeholder = 'Start writing...' }) => {
  const editor = useEditor({
    extensions: [
      StarterKit,
      Link.configure({
        openOnClick: false,
      }),
      Image,
      TextAlign.configure({
        types: ['heading', 'paragraph'],
      }),
    ],
    content,
    onUpdate: ({ editor }) => {
      onChange(editor.getHTML());
    },
    editorProps: {
      attributes: {
        class: 'prose prose-sm sm:prose lg:prose-lg xl:prose-2xl mx-auto focus:outline-none min-h-[200px] p-4',
      },
    },
  });

  return (
    <div className="border border-gray-300 rounded-lg overflow-hidden">
      <EditorToolbar editor={editor} />
      <div className="bg-white">
        <EditorContent
          editor={editor}
          placeholder={placeholder}
        />
      </div>
    </div>
  );
};

export default TextEditor;