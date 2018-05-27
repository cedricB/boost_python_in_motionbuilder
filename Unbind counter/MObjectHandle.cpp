#include <boost/python.hpp>
#include <fbsdk/fbsdk.h>

#include <string>
#include <stdio.h>


namespace pyRigUtils
{
	class MObjectHandle
	 {
		public:
			MObjectHandle(FBModel_Wrapper* inNode);  
			~MObjectHandle();	
		public:
			bool isValid();

	 private:
		 HdlFBPlug modelHandle;
	};
	
	BOOST_PYTHON_MODULE(pyRigUtils)
	{
	    class_<MObjectHandle>("MObjectHandle", init<FBModel_Wrapper*>())
			.def("isValid", &MObjectHandle::isValid)
		;
	}
}


namespace pyRigUtils
{
	MObjectHandle::MObjectHandle(FBModel_Wrapper* inNode)
	{
		modelHandle =  HdlFBPlug((FBPlug *)inNode->mFBModel) ;
	}

	MObjectHandle::~MObjectHandle()
	{
		modelHandle = NULL;
	}

	bool MObjectHandle::isValid()
	{
		if ( modelHandle.Ok() )
		{
			FBModel* inNode = ((FBModel *)modelHandle.GetPlug());

			if (!inNode)
			{
				return false;
			}

			if (!inNode->GetStatusFlag(FBPlugStatusFlag::kFBOwnedByUndo))
			{
				return true;
			}

			if ( inNode->GetDstCount() == 0 )
			{
				return false
			}

			return true;
		}

		return false;
	}

};
