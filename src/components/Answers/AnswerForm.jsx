import React, { useState } from 'react';
import { useQuestionStore } from '../../context/questionStore';
import { useAuthStore } from '../../context/authStore';
import TextEditor from '../Editor/TextEditor';
import Button from '../UI/Button';
import toast from 'react-hot-toast';

const AnswerForm = ({ questionId }) => {
  const [content, setContent] = useState('');
  const { createAnswer, isLoading } = useQuestionStore();
  const { user } = useAuthStore();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!content.trim()) {
      toast.error('Please enter your answer');
      return;
    }

    try {
      await createAnswer({
        questionId: parseInt(questionId),
        content,
        author: user
      });
      
      setContent('');
      toast.success('Answer posted successfully!');
    } catch (error) {
      toast.error('Failed to post answer');
    }
  };

  if (!user) {
    return (
      <div className="bg-gray-50 rounded-lg p-6 text-center">
        <p className="text-gray-600 mb-4">
          You must be logged in to post an answer.
        </p>
        <Button onClick={() => window.location.href = '/login'}>
          Sign in to answer
        </Button>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Your Answer
      </h3>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <TextEditor
          content={content}
          onChange={setContent}
          placeholder="Write your answer here..."
        />
        
        <div className="flex space-x-3">
          <Button
            type="submit"
            loading={isLoading}
          >
            Post Answer
          </Button>
          
          <Button
            type="button"
            variant="outline"
            onClick={() => setContent('')}
          >
            Clear
          </Button>
        </div>
      </form>

      <div className="mt-4 p-4 bg-blue-50 rounded-lg">
        <h4 className="font-medium text-blue-900 mb-2">Writing a good answer</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Provide step-by-step instructions or explanations</li>
          <li>• Include code examples when relevant</li>
          <li>• Explain why your solution works</li>
          <li>• Consider edge cases and limitations</li>
        </ul>
      </div>
    </div>
  );
};

export default AnswerForm;