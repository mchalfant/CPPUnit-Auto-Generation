#ifndef CAMERA_H_INCLUDED
#define CAMERA_H_INCLUDED

class Camera{
   public:
      bool Process;
      void Setup( void );

   private:
      int counter;
      int ActivateCamera( void );
};

bool CRCValue();

#endif CAMERA_H_INCLUDED
