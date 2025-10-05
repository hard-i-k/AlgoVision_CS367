import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuestionStore } from '../../context/questionStore';
import { useAuthStore } from '../../context/authStore';
import TextEditor from '../Editor/TextEditor';
import TagMultiSelect from '../Tags/TagMultiSelect';
import Button from '../UI/Button';
import toast from 'react-hot-toast';

const AskQuestionForm = () => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    tags: []
  });
  
  const { createQuestion, isLoading } = useQuestionStore();
  const { user, isAuthenticated } = useAuthStore();
  const navigate = useNavigate();

  // Redirect if not authenticated
  React.useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    }
  }, [isAuthenticated, navigate]);

  // Show loading if checking authentication
  if (!isAuthenticated) {
    return (
      <div className="flex justify-center items-center min-h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Checking authentication...</p>
        </div>
      </div>
    );
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!isAuthenticated) {
      toast.error('Please log in to ask a question');
      navigate('/login');
      return;
    }
    
    if (!formData.title.trim()) {
      toast.error('Please enter a title');
      return;
    }
    
    if (formData.title.trim().length < 10) {
      toast.error('Title must be at least 10 characters long');
      return;
    }
    
    if (formData.title.trim().length > 200) {
      toast.error('Title must be less than 200 characters');
      return;
    }
    
    if (!formData.description.trim()) {
      toast.error('Please enter a description');
      return;
    }
    
    if (formData.description.trim().length < 20) {
      toast.error('Description must be at least 20 characters long');
      return;
    }
    
    if (formData.description.trim().length > 5000) {
      toast.error('Description must be less than 5000 characters');
      return;
    }
    
    if (formData.tags.length === 0) {
      toast.error('Please add at least one tag');
      return;
    }
    
    if (formData.tags.length > 10) {
      toast.error('You can add at most 10 tags');
      return;
    }

    try {
      const questionData = {
        title: formData.title,
        description: formData.description,
        tags: formData.tags
      };
      
      const newQuestion = await createQuestion(questionData);
      toast.success('Question posted successfully!');
      navigate(`/questions/${newQuestion.id}`);
    } catch (error) {
      console.error('Error creating question:', error);
      toast.error(error.message || 'Failed to post question');
    }
  };

  const handleChange = (field, value) => {
    setFormData({
      ...formData,
      [field]: value
    });
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Ask a Question</h1>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Title */}
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
              Title
            </label>
            <input
              type="text"
              id="title"
              value={formData.title}
              onChange={(e) => handleChange('title', e.target.value)}
              placeholder="What's your programming question?"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              maxLength={200}
            />
            <p className="text-xs text-gray-500 mt-1">
              Be specific and imagine you're asking a question to another person (10-200 characters)
              <span className={`ml-2 ${formData.title.length > 200 ? 'text-red-500' : ''}`}>
                {formData.title.length}/200
              </span>
            </p>
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Description
            </label>
            <TextEditor
              content={formData.description}
              onChange={(content) => handleChange('description', content)}
              placeholder="Describe your problem in detail. Include any code, error messages, or steps you've tried."
            />
            <p className="text-xs text-gray-500 mt-1">
              Include all the information someone would need to identify and solve your problem (20-5000 characters)
            </p>
          </div>

          {/* Tags */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Tags
            </label>
            <TagMultiSelect
              selectedTags={formData.tags}
              onChange={(tags) => handleChange('tags', tags)}
              placeholder="Add up to 5 tags to describe what your question is about"
            />
            <p className="text-xs text-gray-500 mt-1">
              Add tags to help others find and answer your question (max 10 tags)
            </p>
          </div>

          {/* Submit buttons */}
          <div className="flex space-x-3">
            <Button
              type="submit"
              loading={isLoading}
              className="px-6"
            >
              Post Question
            </Button>
            
            <Button
              type="button"
              variant="outline"
              onClick={() => navigate('/')}
            >
              Cancel
            </Button>
          </div>
        </form>

        {/* Guidelines */}
        <div className="mt-8 p-4 bg-blue-50 rounded-lg">
          <h3 className="font-medium text-blue-900 mb-2">Writing a good question</h3>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• Summarize your problem in a one-line title</li>
            <li>• Describe your problem in more detail</li>
            <li>• Describe what you tried and what you expected to happen</li>
            <li>• Add relevant tags to help others find your question</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default AskQuestionForm;