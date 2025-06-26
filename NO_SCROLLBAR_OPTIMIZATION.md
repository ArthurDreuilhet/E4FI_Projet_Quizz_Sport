# Optimisation Anti-Scrollbar

## Problème résolu
L'application avait des barres de défilement qui apparaissaient lors de la navigation entre les questions, dépassant de la fenêtre du navigateur.

## Solutions mises en place

### 1. Configuration globale (base.css)
- `html` et `body` configurés avec `overflow: hidden`
- `body` configuré en `position: fixed` pour garantir qu'il reste dans la fenêtre
- `max-width: 100%` sur tous les éléments pour éviter les débordements horizontaux

### 2. Container principal (App.vue)
- `.app-container` configuré en `position: fixed` 
- Dimensions strictes : `100vh` × `100vw`
- `overflow: hidden` pour empêcher tout débordement

### 3. Page des questions (Question.vue)
- `.question-page-container` utilise `height: calc(90vh - 40px)` au lieu de `100vh`
- `overflow: hidden` pour empêcher le débordement
- Réduction des espaces et marges pour optimiser l'utilisation de l'espace
- `flex-shrink: 0` sur les éléments fixes (header, navigation)

### 4. Composant QuestionDisplay (QuestionDisplay.vue)
- Container adapté à `height: 100%` pour utiliser tout l'espace parent
- Images limitées à `max-height: 150px` (au lieu de 200px)
- Réduction des paddings et marges
- Liste des réponses avec scroll interne uniquement si nécessaire
- `padding-right: 5px` pour la scrollbar interne des réponses

## Responsive Design
- Ajustements spécifiques pour mobile (768px et moins)
- Réduction supplémentaire des espaces et tailles de police
- Images encore plus petites sur mobile (120px)

## Résultat
✅ Aucune barre de défilement visible lors de la navigation entre questions
✅ Interface adaptée à toutes les tailles d'écran
✅ Scroll interne uniquement pour les listes de réponses si nécessaire
✅ Utilisation optimale de l'espace disponible

## Notes techniques
- La navigation entre questions ne provoque plus de changements de hauteur
- Le layout est maintenant entièrement prévisible et contrôlé
- Les éléments sont dimensionnés de manière relative pour s'adapter automatiquement
