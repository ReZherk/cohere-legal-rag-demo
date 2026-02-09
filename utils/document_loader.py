"""
Utilidades para cargar y procesar documentos Markdown
"""
import os
from typing import List, Dict
from pathlib import Path


class Document:
    """
    Representa un documento con su contenido y metadatos
    """
    def __init__(self, content: str, metadata: Dict[str, str]):
        self.content = content
        self.metadata = metadata
    
    def __repr__(self):
        return f"Document(source={self.metadata.get('source', 'unknown')})"


class DocumentLoader:
    """
    Carga documentos desde archivos Markdown
    """
    
    @staticmethod
    def load_markdown_file(file_path: str) -> Document:
        """
        Carga un archivo Markdown individual
        
        Args:
            file_path: Ruta al archivo .md
            
        Returns:
            Document con el contenido y metadatos
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        metadata = {
            'source': os.path.basename(file_path),
            'path': file_path,
            'type': 'markdown'
        }
        
        return Document(content=content, metadata=metadata)
    
    @staticmethod
    def load_from_folder(folder_path: str) -> List[Document]:
        """
        Carga todos los archivos .md de una carpeta
        
        Args:
            folder_path: Ruta a la carpeta con archivos .md
            
        Returns:
            Lista de Documents
        """
        documents = []
        folder = Path(folder_path)
        
        if not folder.exists():
            raise ValueError(f"La carpeta {folder_path} no existe")
        
        # Buscar todos los archivos .md
        md_files = list(folder.glob("*.md"))
        
        if not md_files:
            print(f"⚠️ No se encontraron archivos .md en {folder_path}")
            return documents
        
        for md_file in md_files:
            try:
                doc = DocumentLoader.load_markdown_file(str(md_file))
                documents.append(doc)
                print(f"✅ Cargado: {md_file.name}")
            except Exception as e:
                print(f"❌ Error cargando {md_file.name}: {e}")
        
        return documents
    
    @staticmethod
    def chunk_document(document: Document, chunk_size: int = 500) -> List[Document]:
        """
        Divide un documento en chunks más pequeños
        (Útil para documentos muy largos)
        
        Args:
            document: Documento a dividir
            chunk_size: Tamaño aproximado de cada chunk en caracteres
            
        Returns:
            Lista de Documents (chunks)
        """
        content = document.content
        chunks = []
        
        # Simple splitting por párrafos
        paragraphs = content.split('\n\n')
        current_chunk = ""
        chunk_idx = 0
        
        for para in paragraphs:
            if len(current_chunk) + len(para) < chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    metadata = document.metadata.copy()
                    metadata['chunk_id'] = chunk_idx
                    chunks.append(Document(content=current_chunk.strip(), metadata=metadata))
                    chunk_idx += 1
                current_chunk = para + "\n\n"
        
        # Agregar el último chunk
        if current_chunk:
            metadata = document.metadata.copy()
            metadata['chunk_id'] = chunk_idx
            chunks.append(Document(content=current_chunk.strip(), metadata=metadata))
        
        return chunks
