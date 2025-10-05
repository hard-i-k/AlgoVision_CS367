import React, { useState } from 'react';
import { XMarkIcon } from '@heroicons/react/24/outline';

const TagMultiSelect = ({ selectedTags, onChange, placeholder = 'Add tags...' }) => {
  const [inputValue, setInputValue] = useState('');
  const [suggestions] = useState([
    'javascript', 'react', 'css', 'html', 'nodejs', 'python', 'typescript',
    'vue', 'angular', 'mongodb', 'sql', 'git', 'docker', 'aws', 'frontend',
    'backend', 'fullstack', 'api', 'database', 'authentication', 'routing'
  ]);

  const addTag = (tag) => {
    if (tag && !selectedTags.includes(tag)) {
      onChange([...selectedTags, tag]);
      setInputValue('');
    }
  };

  const removeTag = (tagToRemove) => {
    onChange(selectedTags.filter(tag => tag !== tagToRemove));
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault();
      const tag = inputValue.trim().toLowerCase();
      if (tag) {
        addTag(tag);
      }
    }
  };

  const filteredSuggestions = suggestions.filter(
    tag => 
      tag.toLowerCase().includes(inputValue.toLowerCase()) &&
      !selectedTags.includes(tag)
  );

  return (
    <div className="space-y-2">
      {/* Selected Tags */}
      {selectedTags.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {selectedTags.map((tag, index) => (
            <span
              key={index}
              className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
            >
              {tag}
              <button
                onClick={() => removeTag(tag)}
                className="ml-1 text-blue-600 hover:text-blue-800"
              >
                <XMarkIcon className="w-3 h-3" />
              </button>
            </span>
          ))}
        </div>
      )}

      {/* Input */}
      <div className="relative">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={placeholder}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />

        {/* Suggestions */}
        {inputValue && filteredSuggestions.length > 0 && (
          <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-300 rounded-lg shadow-lg z-10 max-h-32 overflow-y-auto">
            {filteredSuggestions.slice(0, 5).map((suggestion, index) => (
              <button
                key={index}
                onClick={() => addTag(suggestion)}
                className="w-full px-3 py-2 text-left hover:bg-gray-100 first:rounded-t-lg last:rounded-b-lg"
              >
                {suggestion}
              </button>
            ))}
          </div>
        )}
      </div>

      <p className="text-xs text-gray-500">
        Press Enter or comma to add tags. Click suggestions to add them.
      </p>
    </div>
  );
};

export default TagMultiSelect;