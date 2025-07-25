// This is the console version of the glass box script
// To use it, open your browser's developer console (F12 or Cmd+Option+I on Mac)
// and paste this entire script

(function() {
    'use strict';
    
    // Function to create the glass box with a string input
    function createGlassBox(inputString = "Welcome to your glass box\nAdd multiple lines\nEach becomes a bullet point") {
        // Parse input string into bullet points
        const bulletPoints = inputString.split('\n').filter(line => line.trim() !== '');
        
        // Create the main container
        const glassBox = document.createElement('div');
        glassBox.id = 'tm-glass-box';
        
        // Apply glassmorphism styles
        const styles = `
            #tm-glass-box {
                position: fixed;
                top: 20px;
                left: 20px;
                width: 300px;
                padding: 20px;
                background: rgba(255, 255, 255, 0.15);
                backdrop-filter: blur(12px) saturate(180%);
                -webkit-backdrop-filter: blur(12px) saturate(180%);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 16px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1), 
                            inset 0 0 0 1px rgba(255, 255, 255, 0.2);
                color: rgba(0, 0, 0, 0.8);
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', sans-serif;
                z-index: 9999;
                cursor: move;
                user-select: none;
                transition: transform 0.2s ease;
                overflow: hidden;
            }
            
            #tm-glass-box::after {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(
                    135deg,
                    rgba(255, 255, 255, 0.4) 0%,
                    rgba(255, 255, 255, 0.1) 50%,
                    rgba(255, 255, 255, 0) 100%
                );
                border-radius: 16px;
                z-index: -1;
            }
            
            #tm-glass-box:active {
                transform: scale(1.02);
            }
            
            #tm-glass-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
                padding-bottom: 10px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            #tm-glass-title {
                font-weight: 600;
                font-size: 16px;
                color: rgba(0, 0, 0, 0.8);
            }
            
            #tm-glass-close {
                width: 20px;
                height: 20px;
                border-radius: 50%;
                background: rgba(255, 100, 100, 0.8);
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                font-size: 14px;
                color: white;
                border: none;
                outline: none;
            }
            
            #tm-glass-content {
                padding: 5px 0;
            }
            
            #tm-glass-content ul {
                margin: 0;
                padding: 0 0 0 20px;
            }
            
            #tm-glass-content li {
                margin-bottom: 8px;
                line-height: 1.4;
                color: rgba(0, 0, 0, 0.7);
            }
        `;
        
        // Add styles to the document
        const styleElement = document.createElement('style');
        styleElement.textContent = styles;
        document.head.appendChild(styleElement);
        
        // Create header with title and close button
        const header = document.createElement('div');
        header.id = 'tm-glass-header';
        
        const title = document.createElement('div');
        title.id = 'tm-glass-title';
        title.textContent = 'Glass Box';
        
        const closeButton = document.createElement('button');
        closeButton.id = 'tm-glass-close';
        closeButton.textContent = '×';
        closeButton.addEventListener('click', () => {
            document.body.removeChild(glassBox);
        });
        
        header.appendChild(title);
        header.appendChild(closeButton);
        
        // Create content container
        const content = document.createElement('div');
        content.id = 'tm-glass-content';
        
        // Create bullet points list
        const list = document.createElement('ul');
        bulletPoints.forEach(point => {
            const listItem = document.createElement('li');
            listItem.textContent = point;
            list.appendChild(listItem);
        });
        
        content.appendChild(list);
        
        // Assemble the box
        glassBox.appendChild(header);
        glassBox.appendChild(content);
        
        // Add to the document
        document.body.appendChild(glassBox);
        
        // Make the box draggable
        let isDragging = false;
        let offsetX, offsetY;
        
        glassBox.addEventListener('mousedown', (e) => {
            isDragging = true;
            offsetX = e.clientX - glassBox.getBoundingClientRect().left;
            offsetY = e.clientY - glassBox.getBoundingClientRect().top;
            glassBox.style.cursor = 'grabbing';
        });
        
        document.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            
            const x = e.clientX - offsetX;
            const y = e.clientY - offsetY;
            
            glassBox.style.left = `${x}px`;
            glassBox.style.top = `${y}px`;
        });
        
        document.addEventListener('mouseup', () => {
            isDragging = false;
            glassBox.style.cursor = 'grab';
        });
        
        return glassBox;
    }
    
    // Create a function that can be called from the console
    window.addGlassBox = function(text) {
        return createGlassBox(text);
    };
    
    // Create a default glass box
    createGlassBox();
    
    console.log('Glass box created! You can create more boxes by calling: addGlassBox("Your text\\nWith bullet points")');
})();
