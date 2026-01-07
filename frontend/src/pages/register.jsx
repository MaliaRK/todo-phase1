import React from 'react';
import RegisterForm from '../components/Auth/Register';
import Head from 'next/head';

const RegisterPage = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <Head>
        <title>Register - Todo App</title>
        <meta name="description" content="Create a new account for the Todo app" />
      </Head>

      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h1 className="text-center text-3xl font-extrabold text-gray-900">
          Todo App
        </h1>
        <p className="mt-2 text-center text-sm text-gray-600">
          Create a new account 
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md bg-red-400">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <RegisterForm />
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;