import React, { useState } from 'react';
import {
  BoldIcon,
  ItalicIcon,
  UnderlineIcon,
  LinkIcon,
  PhotoIcon,
  FaceSmileIcon,
  ListBulletIcon,
  Bars3BottomLeftIcon,
  Bars3Icon,
  Bars3BottomRightIcon
} from '@heroicons/react/24/outline';

const EditorToolbar = ({ editor }) => {
  const [showLinkInput, setShowLinkInput] = useState(false);
  const [linkUrl, setLinkUrl] = useState('');
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);

  if (!editor) return null;

  const addLink = () => {
    if (linkUrl) {
      editor.chain().focus().setLink({ href: linkUrl }).run();
      setLinkUrl('');
      setShowLinkInput(false);
    }
  };

  const addImage = () => {
    const url = prompt('Enter image URL:');
    if (url) {
      editor.chain().focus().setImage({ src: url }).run();
    }
  };

  const addEmoji = (emoji) => {
    editor.chain().focus().insertContent(emoji).run();
    setShowEmojiPicker(false);
  };

  const commonEmojis = ['😀', '😂', '😊', '😍', '🤔', '👍', '👎', '❤️', '🔥', '💯'];

  return (
    <div className="bg-gray-50 border-b border-gray-300 p-2 flex flex-wrap gap-1">
      {/* Text Formatting */}
      <button
        onClick={() => editor.chain().focus().toggleBold().run()}
        className={`p-2 rounded hover:bg-gray-200 ${
          editor.isActive('bold') ? 'bg-gray-300' : ''
        }`}
        title="Bold"
      >
        <BoldIcon className="w-4 h-4" />
      </button>

      <button
        onClick={() => editor.chain().focus().toggleItalic().run()}
        className={`p-2 rounded hover:bg-gray-200 ${
          editor.isActive('italic') ? 'bg-gray-300' : ''
        }`}
        title="Italic"
      >
        <ItalicIcon className="w-4 h-4" />
      </button>

      <button
        onClick={() => editor.chain().focus().toggleStrike().run()}
        className={`p-2 rounded hover:bg-gray-200 ${
          editor.isActive('strike') ? 'bg-gray-300' : ''
        }`}
        title="Strikethrough"
      >
        <UnderlineIcon className="w-4 h-4" />
      </button>

      <div className="w-px bg-gray-300 mx-1"></div>

      {/* Lists */}
      <button
        onClick={() => editor.chain().focus().toggleBulletList().run()}
        className={`p-2 rounded hover:bg-gray-200 ${
          editor.isActive('bulletList') ? 'bg-gray-300' : ''
        }`}
        title="Bullet List"
      >
        <ListBulletIcon className="w-4 h-4" />
      </button>

      <button
        onClick={() => editor.chain().focus().toggleOrderedList().run()}
        className={`p-2 rounded hover:bg-gray-200 ${
          editor.isActive('orderedList') ? 'bg-gray-300' : ''
        }`}
        title="Numbered List"
      >
        <Bars3Icon className="w-4 h-4" />
      </button>

      <div className="w-px bg-gray-300 mx-1"></div>

      {/* Alignment */}
      <button
        onClick={() => editor.chain().focus().setTextAlign('left').run()}
        className={`p-2 rounded hover:bg-gray-200 ${
          editor.isActive({ textAlign: 'left' }) ? 'bg-gray-300' : ''
        }`}
        title="Align Left"
      >
        <Bars3BottomLeftIcon className="w-4 h-4" />
      </button>

      <button
        onClick={() => editor.chain().focus().setTextAlign('center').run()}
        className={`p-2 rounded hover:bg-gray-200 ${
          editor.isActive({ textAlign: 'center' }) ? 'bg-gray-300' : ''
        }`}
        title="Align Center"
      >
        <Bars3Icon className="w-4 h-4" />
      </button>

      <button
        onClick={() => editor.chain().focus().setTextAlign('right').run()}
        className={`p-2 rounded hover:bg-gray-200 ${
          editor.isActive({ textAlign: 'right' }) ? 'bg-gray-300' : ''
        }`}
        title="Align Right"
      >
        <Bars3BottomRightIcon className="w-4 h-4" />
      </button>

      <div className="w-px bg-gray-300 mx-1"></div>

      {/* Link */}
      <div className="relative">
        <button
          onClick={() => setShowLinkInput(!showLinkInput)}
          className="p-2 rounded hover:bg-gray-200"
          title="Add Link"
        >
          <LinkIcon className="w-4 h-4" />
        </button>
        
        {showLinkInput && (
          <div className="absolute top-full left-0 mt-1 bg-white border border-gray-300 rounded-lg p-2 shadow-lg z-10">
            <input
              type="url"
              placeholder="Enter URL"
              value={linkUrl}
              onChange={(e) => setLinkUrl(e.target.value)}
              className="w-48 px-2 py-1 border border-gray-300 rounded text-sm"
              onKeyPress={(e) => e.key === 'Enter' && addLink()}
            />
            <div className="flex gap-1 mt-1">
              <button
                onClick={addLink}
                className="px-2 py-1 bg-blue-600 text-white text-xs rounded hover:bg-blue-700"
              >
                Add
              </button>
              <button
                onClick={() => setShowLinkInput(false)}
                className="px-2 py-1 bg-gray-300 text-xs rounded hover:bg-gray-400"
              >
                Cancel
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Image */}
      <button
        onClick={addImage}
        className="p-2 rounded hover:bg-gray-200"
        title="Add Image"
      >
        <PhotoIcon className="w-4 h-4" />
      </button>

      {/* Emoji */}
      <div className="relative">
        <button
          onClick={() => setShowEmojiPicker(!showEmojiPicker)}
          className="p-2 rounded hover:bg-gray-200"
          title="Add Emoji"
        >
          <FaceSmileIcon className="w-4 h-4" />
        </button>
        
        {showEmojiPicker && (
          <div className="absolute top-full left-0 mt-1 bg-white border border-gray-300 rounded-lg p-2 shadow-lg z-10">
            <div className="grid grid-cols-5 gap-1">
              {commonEmojis.map((emoji, index) => (
                <button
                  key={index}
                  onClick={() => addEmoji(emoji)}
                  className="p-1 hover:bg-gray-100 rounded text-lg"
                >
                  {emoji}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default EditorToolbar;