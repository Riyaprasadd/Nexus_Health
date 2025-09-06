import i18n from "i18next";
import { initReactI18next } from "react-i18next";

const resources = {
  en: {
    translation: {
      login: "Login",
      register: "Register",
      resetPassword: "Reset Password",
      chatbot: "Chatbot",
      username: "Username",
      email: "Email",
      age: "Age",
      gender: "Gender",
      password: "Password",
      submit: "Submit",
      language: "Language"
    }
  },
  hi: {
    translation: {
      login: "लॉगिन",
      register: "रजिस्टर",
      resetPassword: "पासवर्ड रीसेट",
      chatbot: "चैटबॉट",
      username: "उपयोगकर्ता नाम",
      email: "ईमेल",
      age: "उम्र",
      gender: "लिंग",
      password: "पासवर्ड",
      submit: "जमा करें",
      language: "भाषा"
    }
  },
  es: {
    translation: {
      login: "Iniciar sesión",
      register: "Registrar",
      resetPassword: "Restablecer contraseña",
      chatbot: "Chatbot",
      username: "Nombre de usuario",
      email: "Correo electrónico",
      age: "Edad",
      gender: "Género",
      password: "Contraseña",
      submit: "Enviar",
      language: "Idioma"
    }
  },
  fr: {
    translation: {
      login: "Connexion",
      register: "S'inscrire",
      resetPassword: "Réinitialiser le mot de passe",
      chatbot: "Chatbot",
      username: "Nom d'utilisateur",
      email: "E-mail",
      age: "Âge",
      gender: "Genre",
      password: "Mot de passe",
      submit: "Soumettre",
      language: "Langue"
    }
  }
};

i18n.use(initReactI18next).init({
  resources,
  lng: "en", // default language
  interpolation: {
    escapeValue: false
  }
});

export default i18n;
